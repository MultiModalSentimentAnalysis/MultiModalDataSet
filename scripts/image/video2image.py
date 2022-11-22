from settings import DATA_DIR
from glob import glob
import cv2
from random import randrange
import os
from tqdm import tqdm


def read_frames(video_path: str):
    cam = cv2.VideoCapture(video_path)
    frames = list()
    while(True):
        ret, frame = cam.read()
        if ret:
            frames.append(frame)
        else:
            break
    cam.release()
    cv2.destroyAllWindows()
    return frames


def select_frame(frames: list):
    n = len(frames)
    frame_ind = randrange(n)
    selected_frame = frames[frame_ind]
    return selected_frame, frame_ind


def vid2img(video_path: str):
    frames = read_frames(video_path)
    selected_frame, index = select_frame(frames)
    movie_path = "".join(video_path.split("clips")[:-1])
    clip_name = video_path.split("clips")[-1].split("/")[-1].split(".")[0]
    img_path = f"{movie_path}/images/{clip_name}_image_{index}.png"
    os.makedirs(f"{movie_path}/images", exist_ok=True)
    cv2.imwrite(img_path, selected_frame)
    del frames


if __name__ == "__main__":  
    clip_paths = DATA_DIR / "*" / "clips" / "*.mkv"
    paths = glob(str(clip_paths))
    for path in tqdm(paths):
        vid2img(path)
