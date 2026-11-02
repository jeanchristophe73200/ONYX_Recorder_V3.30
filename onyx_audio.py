import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import time
import os
import queue
from datetime import datetime
import onyx_settings as config

class AudioEngine:
    def __init__(self, callback_file_completed=None):
        self.recording = False
        self.stream = None
        self.q = queue.Queue()
        self.callback = callback_file_completed
        self.current_filename = ""
        self.start_time = 0
        self.file_counter = 0
        self.session_folder = config.RECORD_DIR # Par défaut

    def callback_audio(self, indata, frames, time_info, status):
        if status: print(f"Status Audio: {status}")
        if self.recording:
            self.q.put(indata.copy())

    def start_stream(self):
        try:
            self.stream = sd.InputStream(
                device=config.AUDIO_DEVICE_INDEX,
                channels=1,
                samplerate=config.SAMPLE_RATE,
                blocksize=config.CHUNK_SIZE,
                callback=self.callback_audio
            )
            self.stream.start()
        except Exception as e:
            print(f"Erreur Stream: {e}")

    def stop_stream(self):
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()

    def set_session_folder(self, folder_path):
        """Définit le dossier de la session en cours"""
        self.session_folder = folder_path

    def start_recording(self):
        self.recording = True
        self.file_counter = 0
        threading.Thread(target=self.record_loop, daemon=True).start()

    def get_new_filename(self):
        ts = datetime.now().strftime("%Y-%m-%d_%Hh%M")
        # On enregistre DANS le dossier de session défini
        filename = f"{ts}_Audio.flac"
        return os.path.join(self.session_folder, filename)

    def record_loop(self):
        self.start_time = time.time()
        self.current_filename = self.get_new_filename()
        
        # On s'assure que le dossier existe
        if not os.path.exists(self.session_folder):
            os.makedirs(self.session_folder)

        print(f"--- [AUDIO] Début fichier : {os.path.basename(self.current_filename)} ---")
        
        with sf.SoundFile(self.current_filename, mode='w', samplerate=config.SAMPLE_RATE, channels=1) as file:
            while self.recording:
                while not self.q.empty():
                    data = self.q.get()
                    file.write(data)
                
                # Rotation horaire (Toutes les heures pleines)
                elapsed = time.time() - self.start_time
                if elapsed > 10: 
                    now = datetime.now()
                    if now.minute == 0 and now.second < 5:
                         # On ferme le fichier actuel
                        old_file = self.current_filename
                        print(f"--- [AUDIO] Fin de fichier (Rotation) : {os.path.basename(old_file)} ---")
                        break # On sort du write pour relancer la boucle (nouveau fichier)

                time.sleep(0.01)
        
        # Callback fin de fichier
        if self.callback and os.path.exists(self.current_filename):
            self.callback(self.current_filename)

        # Si toujours en enregistrement, on relance un nouveau fichier
        if self.recording:
            self.record_loop()
