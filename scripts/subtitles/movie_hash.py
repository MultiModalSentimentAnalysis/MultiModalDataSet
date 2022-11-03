from asyncio import streams
import struct, os
import requests
import numpy as np
import pandas as pd
from tqdm import tqdm
from glob import glob

API_KEY = "F9A7NgI3wmHGvPrix1Ub4j7SchTKjdLU"
headers = {"Api-Key": API_KEY, "Content-Type": "application/json"}

def hashFile(name): 
      try: 
                 
        longlongformat = '<q'  # little-endian long long
        bytesize = struct.calcsize(longlongformat) 
            
        f = open(name, "rb") 
            
        filesize = os.path.getsize(name) 
        hash = filesize 
            
        if filesize < 65536 * 2: 
            return "SizeError" 
        
        f_range = 65536/bytesize
        f_range = int(f_range)
        for x in range(f_range): 
            buffer = f.read(bytesize) 
            (l_value,)= struct.unpack(longlongformat, buffer)  
            hash += l_value 
            hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
                

        f.seek(max(0,filesize-65536),0) 
        for x in range(f_range): 
            buffer = f.read(bytesize) 
            (l_value,)= struct.unpack(longlongformat, buffer)  
            hash += l_value 
            hash = hash & 0xFFFFFFFFFFFFFFFF 
            
        f.close() 
        returnedhash =  "%016x" % hash 
        return returnedhash 
    
      except(IOError): 
        return "IOError"

def download_subtitle(file_id):
    download_url = "https://api.opensubtitles.com/api/v1/download"
    str_body = {"file_id": file_id}
    # request_text = f"""curl --request POST --url {download_url} --header 'Api-Key: {API_KEY}' --header 'Content-Type: application/json' --data '{str_body}'"""
    headers = {'Api-Key': API_KEY, 'Content-Type': 'application/json'}
    response = requests.post(url=download_url, headers=headers, data=str_body)



def search_subtitle(movie_path, movie_hash=None, api_key=None, imdb_id=0, languages="en"):
    subtitle_url = "https://api.opensubtitles.com/api/v1/subtitles"
    if not movie_hash:  
        moviehash = hashFile(movie_path)

    parameters = {"moviehash": moviehash, "languages": languages}
    if imdb_id!=0:
        parameters["imdb_id"] = imdb_id
    results = requests.get(url=subtitle_url, headers=headers, params=parameters).json()
    data = results["data"]
    return data[0]


def get_movie_path(file_name):
    dir_path = f"videos/{file_name}/{file_name}"
    extensions = [".mkv", ".mp4", ".avi"]
    for exten in extensions:
        file_addr = f"{dir_path}{exten}"
        print(file_addr)
        if os.path.exists(file_addr):
            return file_addr
    return ""


def prepare_movies_for_opensubtitle(movie_df, path=None):
    movie_df["movie_path"] = movie_df["file_name"].apply(get_movie_path)
    movie_df = movie_df.replace("", np.nan)
    movie_df = movie_df.dropna(subset=["movie_path"])
    movie_df["imdb_id_clean"] = movie_df["imdb_id"].apply(lambda x: int(x.replace("tt", "")))
    movie_df["movie_hash"] = movie_df["movie_path"].apply(lambda x: hashFile(x))
    if path:
        movie_df.to_csv(path)
    return movie_df