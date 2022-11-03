import os
import sys
import pysrt
import numpy as np
import pandas as pd
from tqdm import tqdm
from glob import glob
from math import floor
from pathlib import Path
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
sys.path.append(str(Path(".").resolve()))
from settings import DATA_DIR, VIDEO_DIR

# Reencoding results in exact cuts, but it is slower
RE_ENCODE = True

movies_df = pd.read_csv("movies.csv")
error_file = open("logs/cutlip-subtitles-errors.log", "w")
# movies_df["file_name"][movies_df["file_name"].str.endswith("'/")] = movies_df[
#     "file_name"
# ].apply(lambda x: x[:-2])

extensions = ["mkv", "mp4", "avi"]
movie_paths = []
for extension in extensions:
    movie_paths.extend(glob(str(VIDEO_DIR / "**" / ("*." + extension))))

for i, movie_path in enumerate(movie_paths):
    print(
        f"--------------------- {i+1}/{len(movie_paths)}------------------------------------"
    )
    try:
        filename = os.path.basename(movie_path)
        print(filename)
        extension = filename.split(".")[-1]
        movie_name = ".".join(filename.split(".")[:-1])

        row = movies_df.loc[movies_df.file_name == movie_name]
        if len(row) == 0:
            print(f"Error loading movie {movie_name}. No entry in the sheet.")
            continue
        if len(row) > 1:
            print(f"Error loading movie {movie_name}. Multiple entries.")
            continue

        row = row.iloc[0]
        is_invalid = row["is_invalid"]
        if is_invalid:
            print(f"Error loading movie {movie_name}. Movie is invalid")
            continue

        movie_id = row["id"]
        
        sub_path = VIDEO_DIR / movie_name / (movie_name + "-opensubtitle.srt")
        try:
            subs = pysrt.open(sub_path)
        except:
            print(f"Error loading subtitle for {movie_name}")
            error_file.write(movie_name)
            error_file.write("\n")
            continue

        MOVIE_BASE_DIR = DATA_DIR / str(movie_id)
        CLIPS_DIR = MOVIE_BASE_DIR / "clips"
        if not os.path.exists(MOVIE_BASE_DIR):
            os.mkdir(MOVIE_BASE_DIR)
        if not os.path.exists(CLIPS_DIR):
            os.mkdir(CLIPS_DIR)

        movie = VideoFileClip(movie_path)
        duration = movie.duration
        number_of_samples = floor(
            duration / 30
        )  # number of samples ~ length of video in minutes
        if len(subs) < number_of_samples:
            number_of_samples = len(subs)
        step = floor(len(subs) / number_of_samples)
        sub_indexes = np.arange(number_of_samples) * step + 1

        texts = []
        for clip_index, sub_index in enumerate(tqdm(sub_indexes)):
            sub = subs[sub_index - 1]
            text = sub.text
            if not text.isascii():
                continue
            start = sub.start
            end = sub.end
            start = (
                start.hours * 3600
                + start.minutes * 60
                + start.seconds
                + start.milliseconds / 1000
            )
            end = (
                end.hours * 3600
                + end.minutes * 60
                + end.seconds
                + end.milliseconds / 1000
            )
            texts.append((sub_index, text.replace("\n", " ")))

            clip = VideoFileClip(movie_path).subclip(start, end)
            clip_path = CLIPS_DIR / f"clip_{clip_index}.mkv"
            if RE_ENCODE:
                clip.write_videofile(
                    str(clip_path),
                    logger=None,
                    codec="libx264",
                    temp_audiofile="temp-audio.m4a",
                    remove_temp=True,
                    audio_codec="aac",
                )
            else:
                ffmpeg_extract_subclip(movie_path, start, end, targetname=clip_path)

        TEXTS_PATH = MOVIE_BASE_DIR / "texts.txt"
        with open(TEXTS_PATH, "w") as text_file:
            for index, text in texts:
                text_file.write(str(index) + "-" + text + "\n")
    except Exception as e:
        print(f"Error for movie path: {movie_path}:", e)
error_file.close()