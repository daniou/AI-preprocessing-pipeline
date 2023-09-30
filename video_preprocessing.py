import os

import librosa
import moviepy.editor as mp
import config

from audio_preprocessing import AudioPreprocessing


class VideoPreprocessing:
    def __init__(self, video_path):
        self.downsampled_video_path = None
        self.downsampled_audio_path = None
        self.video_path = video_path

    def split_video(self, intervals, output_dir):
        print("---+++", self.downsampled_video_path)
        clip = mp.VideoFileClip(self.downsampled_video_path)

        # Crea el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)

        for i, interval in enumerate(intervals):
            start_time = interval[0]
            end_time = interval[1]

            # Genera el nombre de archivo de salida para el subclip
            base_filename = os.path.splitext(os.path.basename(self.video_path))[0]
            subclip_filename = f"{base_filename}_{i}.mp4"
            subclip_path = os.path.join(output_dir, subclip_filename)

            subclip = clip.subclip(start_time, end_time).set_audio(None)

            subclip.write_videofile(subclip_path, codec="libx264")

    def split_video_in_talking_intervals(self, output_path):
        audio_preprocessing = AudioPreprocessing(self.downsampled_audio_path)
        intervals = audio_preprocessing.split_audio_by_silence()

        output_dir = os.path.dirname(output_path)
        print("------", self.downsampled_audio_path)
        audio_preprocessing.save_audio_intervals(intervals, output_dir)
        sr = librosa.get_samplerate(self.downsampled_audio_path)
        intervals_in_seconds = intervals/22000

        self.split_video(intervals_in_seconds, output_dir)

    def downsample_video(self, output_path, target_fps=config.TARGET_VIDEO_FPS,
                         resolution_scale=config.TARGET_VIDEO_RESOLUTION_SCALE,
                         audio_samplerate=config.TARGET_AUDIO_SAMPLERATE,
                         audio_bitrate=config.TARGET_AUDIO_BITRATE):
        print("lo que llega ", output_path)
        video = mp.VideoFileClip(self.video_path)

        # Extraer el audio y guardar el archivo mp3
        audio = video.audio
        audio_path = output_path.replace(".mp4", ".mp3")
        self.downsampled_audio_path = audio_path
        audio.write_audiofile(audio_path, fps=audio_samplerate, bitrate=audio_bitrate, logger=None)

        # Reducción proporcional del ancho y alto
        new_width = int(video.size[0] * resolution_scale)
        new_height = int(video.size[1] * resolution_scale)
        target_resolution = (new_width, new_height)

        video = video.resize(target_resolution)
        video = video.set_audio(None)  # Desactivar el audio
        video = video.set_fps(target_fps)
        video.write_videofile(output_path, codec="libx264", audio=False, logger=None)
        self.downsampled_video_path = output_path
        print("#######",self.downsampled_video_path)



