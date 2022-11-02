# Download subtitles from opensubtitle
download_subtitle.sh will read a csv file in current directory named movies.csv. this file should contain 
df_id - id - imdb_id -  name - file_name -  file_type - gray-  is_invalid - movie_path - imdb_id_clean - movie_hash
columns in specified order. 

<code>movie_hash.prepare_movies_for_opensubtitle
prepare_movies_for_opensubtitle(pd.read_csv("movies.csv"), "movies.csv")
</code> 

the above code will add desired columns to movies.csv file