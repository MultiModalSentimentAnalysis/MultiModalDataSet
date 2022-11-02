import os
import pandas as pd
from glob import glob
from settings import DATA_DIR

def save_input_file(clips, subtitles, path):
    input_dict = {'video' : clips, 'text': subtitles}
    input_df = pd.DataFrame(input_dict)
    input_df.to_csv(path+'input.csv',index = False)

movie_paths = glob((str(DATA_DIR) +'/*/' ))

generate_complete_input_file  = True
total_subtitles = []
total_clips = []
for i, movie_path in enumerate(movie_paths):
    print(
        f"--------------------- {i+1}/{len(movie_paths)}------------------------------------"
    )
    clips = glob(movie_path+'clips/*.mkv')
    with open(movie_path+'texts.txt') as subtitel_file:
        subtitles =  [line.rstrip().split('-',1)[1] for line in subtitel_file]
    if len(subtitles) == len(clips):
        save_input_file(clips, subtitles, movie_path)
        total_subtitles.extend(subtitles)
        total_clips.extend(clips)
    else :
        print('count of clips are not equal to count of subtitels for movie '+ str(movie_path))

if generate_complete_input_file :
    save_input_file(total_clips, total_subtitles, (str(DATA_DIR)+'/'))