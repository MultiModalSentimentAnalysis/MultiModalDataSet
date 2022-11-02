import pandas as pd
from pathlib import Path
from glob import glob
from settings import DATA_DIR, LABELSTUDIO_DIR


def save_input_file(movie_id, clips, subtitles, MOVIE_BASE_DIR):
    clip_ids, clip_paths = zip(*clips)
    input_dict = {"video": clip_paths, "text": subtitles, "clip_id": clip_ids}
    input_df = pd.DataFrame(input_dict)
    input_df["movie_id"] = movie_id
    input_df.to_csv(MOVIE_BASE_DIR / "input.csv", index=False)
    return input_df


movie_paths = glob((str(DATA_DIR) + "/*/"))

generate_complete_input_file = True
movie_dfs = []
for i, MOVIE_BASE_DIR in enumerate(movie_paths):
    print(
        f"--------------------- {i+1}/{len(movie_paths)}------------------------------------"
    )
    MOVIE_BASE_DIR = Path(MOVIE_BASE_DIR)
    movie_id = MOVIE_BASE_DIR.name
    CLIPS_DIR = MOVIE_BASE_DIR / "clips"
    clips = glob(str(CLIPS_DIR / "*.mkv"))
    clips = list(
        map(lambda x: (int(x.rsplit("/")[-1].rsplit(".")[0].split("_")[1]), x), clips)
    )
    clips = sorted(clips)
    with open(MOVIE_BASE_DIR / "texts.txt") as subtitel_file:
        subtitles = [line.rstrip().split("-", 1)[1] for line in subtitel_file]
    if len(subtitles) == len(clips):
        movie_df = save_input_file(movie_id, clips, subtitles, MOVIE_BASE_DIR)
        movie_dfs.append(movie_df)
    else:
        print(
            "count of clips are not equal to count of subtitels for movie "
            + str(MOVIE_BASE_DIR)
        )

if generate_complete_input_file:
    df = pd.concat(movie_dfs, ignore_index=True)
    df.to_csv(LABELSTUDIO_DIR / "input.csv", index=False)
