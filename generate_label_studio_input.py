import os
import pandas as pd
from glob import glob
from settings import DATA_DIR

movie_paths = glob((str(DATA_DIR) +'/*/' ))

for i, movie_path in enumerate(movie_paths):
    print(
        f"--------------------- {i+1}/{len(movie_paths)}------------------------------------"
    )
    clips = glob(movie_path+'clips/*.mkv')
    with open(movie_path+'texts.txt') as subtitel_file:
        subtitels =  [line.rstrip().split('-',1)[1] for line in subtitel_file]
    if len(subtitels) == len(clips):
        input_dict = {'video' : clips, 'text': subtitels}
        input_df = pd.DataFrame(input_dict)
        input_df.to_csv(movie_path+'input.csv',index = False)
    else :
        print('count of clips are not equal to count of subtitels for movie '+ str(movie_path))
