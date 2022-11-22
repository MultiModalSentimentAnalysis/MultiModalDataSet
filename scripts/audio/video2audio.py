from settings import DATA_DIR
from glob import glob
import moviepy.editor as mp
import os
from tqdm import tqdm


def vid2aud(video_path: str):
    movie_path = "".join(video_path.split("clips")[:-1])
    clip_name = video_path.split("clips")[-1].split("/")[-1].split(".")[0]
    audio_path = f"{movie_path}/audios/{clip_name}_audio.wav"
    os.makedirs(f"{movie_path}/audios", exist_ok=True)
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path)


if __name__ == "__main__":  
    clip_paths = DATA_DIR / "*" / "clips" / "*.mkv"
    paths = glob(str(clip_paths))
    for path in tqdm(paths):
        vid2aud(path)