import os

import moviepy.editor as mp
import config

from audio_preprocessing import AudioPreprocessing


class VideoPreprocessing:
    def __init__(self, video_path):
        self.video_path = video_path

    def split_media(self, intervals, output_path):
        clip = mp.VideoFileClip(self.video_path)
        print(self.video_path)
        for i, interval in enumerate(intervals):
            start_time = interval[0] / clip.fps
            end_time = interval[1] / clip.fps

            file_extension = output_path[-3:]
            if 'mp4' in file_extension:
                subclip = clip.subclip(start_time, end_time).set_audio(None)
            else:
                subclip = clip.subclip(start_time, end_time)

            subclip.write_videofile(f"{self.video_path[:-4]}_{i}.{file_extension}", codec="libx264")

    def split_video_in_talking_intervals(self, output_path):
        audio_path = output_path.replace("mp4", "mp3")
        audio_preprocessing = AudioPreprocessing(audio_path)
        intervals = audio_preprocessing.split_audio_by_silence()
        output_dir = os.path.dirname(audio_path)
        audio_preprocessing.save_audio_intervals(intervals, output_dir)
        intervals_in_seconds = intervals/config.TARGET_AUDIO_SAMPLERATE
        print(intervals_in_seconds, output_dir)
        self.split_media(intervals_in_seconds, output_dir)

    def downsample_video(self, output_path, target_fps=config.TARGET_VIDEO_FPS,
                         resolution_scale=config.TARGET_VIDEO_RESOLUTION_SCALE,
                         audio_samplerate=config.TARGET_AUDIO_SAMPLERATE,
                         audio_bitrate=config.TARGET_AUDIO_BITRATE):
        video = mp.VideoFileClip(self.video_path)

        # Extraer el audio y guardar el archivo mp3
        audio = video.audio
        audio_path = output_path.replace(".mp4", ".mp3")
        audio.write_audiofile(audio_path, fps=audio_samplerate, bitrate=audio_bitrate, logger=None)

        # Reducción proporcional del ancho y alto
        new_width = int(video.size[0] * resolution_scale)
        new_height = int(video.size[1] * resolution_scale)
        target_resolution = (new_width, new_height)

        video = video.resize(target_resolution)
        video = video.set_audio(None)  # Desactivar el audio
        video = video.set_fps(target_fps)
        video.write_videofile(output_path, codec="libx264", audio=False, logger=None)
