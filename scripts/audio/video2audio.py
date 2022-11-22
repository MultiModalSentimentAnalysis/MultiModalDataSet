from settings import DATA_DIR
from glob import glob
import moviepy.editor as mp


def vid2aud(video_path: str):
    audio_name = "".join(video_path.split(".")[:-1])
    audio_path = f"{audio_name}.wav"
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)

clip_paths = DATA_DIR / "*" / "clips" / "*.mkv"
paths = glob(str(clip_paths))
for path in paths:
    vid2aud(path)
