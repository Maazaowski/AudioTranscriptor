from api_communication import *

filename = "Files\\Audio.mp3"

audio_url = upload(filename)
save_transcript(audio_url, filename)