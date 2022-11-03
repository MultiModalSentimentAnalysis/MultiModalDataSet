#! /bin/bash
API_KEY="1NGYEzjBLWBqFzkHOu1jDZd2wcLasGLq"

while IFS=, read -r df_id id imdb_id name file_name file_type gray is_invalid movie_path imdb_id_clean movie_hash
do
    echo "processing movie: $name"  
    cmd=$(curl --request GET --url "https://api.opensubtitles.com/api/v1/subtitles?imdb_id=$imdb_id_clean&languages=en&moviehash=$movie_hash" --header "Api-Key: $API_KEY" --header 'Content-Type: application/json')
    file_id=$(echo $cmd | jq .data[0].attributes.files[0].file_id)
    echo "got subtitle for movie $name"
    cmd=$(curl --request POST --url "https://api.opensubtitles.com/api/v1/download" --header "Api-Key: $API_KEY" --header 'Content-Type: application/json' --data '{"file_id":"'"$file_id"'"}')
    dl_link=$(echo $cmd | jq .link | tr -d '"')
    echo "got dl link for $name"
    srt_path="/home/sahel/Downloads/movie/$file_name/$file_name-opensubtitle.srt"
    curl "$dl_link" -o "$srt_path"
    echo "downloaded subtitle for $name"
    # echo "output: $cmd"
done < movies.csv


# res=$(curl --request GET --url "https://api.opensubtitles.com/api/v1/subtitles?imdb_id=34583&languages=en&moviehash=bc20952ce07bab61" --header "Api-Key: F9A7NgI3wmHGvPrix1Ub4j7SchTKjdLU" --header 'Content-Type: application/json')