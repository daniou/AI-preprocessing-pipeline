import librosa
import numpy as np
import os
import soundfile as sf

class AudioPreprocessing:
    def __init__(self, audio_path):
        self.audio_path = audio_path

    def split_audio_by_silence(self, top_db=20):
        # Cargar el archivo de audio
        y, sr = librosa.load(self.audio_path)

        # Detectar segmentos de silencio en el audio
        intervals = librosa.effects.split(y, top_db=top_db, ref=np.max, frame_length=2048, hop_length=512)
        return intervals

    def save_audio_intervals(self, intervals, output_dir):
        y, sr = librosa.load(self.audio_path)
        # Crear un directorio de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Guardar los segmentos de audio como archivos separados
        for i, (start, end) in enumerate(intervals):
            audio_segment = y[start:end]
            output_path = os.path.join(output_dir, f'segment_{i}.wav')
            sf.write(output_path, audio_segment, sr)


