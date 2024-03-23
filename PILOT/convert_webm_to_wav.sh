#!/bin/bash

# Do this before transcription 
for fullfile in DATA/audio_files/*.webm; do 
	filename="${fullfile%.*}"
	wavfilename="$filename"".wav"
	ffmpeg -i "$fullfile" -ac 1 "$wavfilename"
done

# help: https://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash