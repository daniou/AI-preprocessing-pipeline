import librosa
import moviepy.editor as mp
import config
import soundfile as sf





class VideoPreprocessing:
    def __init__(self, video_path):
        self.video_path = video_path

    def save_intervals_as_mp3(self, intervals, output_path):
        for i, interval in enumerate(intervals):
            audio_data = interval
            file_name = f"{output_path[:-4]}_{i}.mp3"
            sf.write(file_name, audio_data, config.TARGET_AUDIO_SAMPLERATE)


    def detect_silence_intervals(self, audio_path,top_db=20):
        print(audio_path)
        y, sr = librosa.load(audio_path)
        intervals = librosa.effects.split(y, top_db=top_db)
        return intervals

    def split_media(self, intervals, output_path):
        clip = mp.VideoFileClip(self.video_path)

        for i, interval in enumerate(intervals):
            start_time = interval[0] / clip.fps
            end_time = interval[1] / clip.fps

            file_extension = output_path[-3:]
            if 'mp4' in file_extension:
                subclip = clip.subclip(start_time, end_time).set_audio(None)
            else:
                subclip = clip.subclip(start_time, end_time)

            subclip.write_videofile(f"{output_path}_{i}.{file_extension}", codec="libx264")

    def split_video_in_talking_intervals(self, output_path):
        audio_path = output_path.replace("mp4", "mp3")
        intervals = self.detect_silence_intervals(audio_path)
        self.save_intervals_as_mp3(intervals,output_path)


    def downsample_video(self, output_path, target_fps=config.TARGET_VIDEO_FPS,
                         resolution_scale=config.TARGET_VIDEO_RESOLUTION_SCALE,
                         audio_samplerate=config.TARGET_AUDIO_SAMPLERATE,
                         audio_bitrate=config.TARGET_AUDIO_BITRATE):
        video = mp.VideoFileClip(self.video_path)

        # Extraer el audio y guardar el archivo mp3
        audio = video.audio
        audio_path = output_path.replace(".mp4", ".mp3")
        audio.write_audiofile(audio_path, fps=audio_samplerate, bitrate=audio_bitrate,  logger=None)

        # Reducción proporcional del ancho y alto
        new_width = int(video.size[0] * resolution_scale)
        new_height = int(video.size[1] * resolution_scale)
        target_resolution = (new_width, new_height)

        video = video.resize(target_resolution)
        video = video.set_audio(None)  # Desactivar el audio
        video = video.set_fps(target_fps)
        video.write_videofile(output_path, codec="libx264", audio=False, logger=None)
