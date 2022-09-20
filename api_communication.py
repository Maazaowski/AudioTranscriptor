import requests
from api_secrets import API_KEY_ASSEMBLYAI
import youtube_dl

upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_KEY_ASSEMBLYAI}


def upload(file_name):
    def read_file(file_name, chunk_size=5242880):
        with open(file_name, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    response = requests.post(upload_endpoint,
                             headers=headers,
                             data=read_file(file_name))

    audio_url = response.json()['upload_url']
    return audio_url


def transcribe(audio_url):
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    job_id = transcript_response.json()['id']
    return job_id


def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
        polling_response = poll(transcript_id)
        if polling_response['status'] == 'completed':
            return polling_response, None
        elif polling_response['status'] == 'error':
            return polling_response, polling_response['error']


def save_transcript(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)

    if data:
        text_file = filename + ".txt"
        with open(text_file, "w") as f:
            f.write(data['text'])
        print("Transcription saved!")
    elif error:
        print("Error! ", error)

def downloadYouTubeAsMp3(link):
    video_info = youtube_dl.YoutubeDL().extract_info(url=link, download=False)
    filename = f"{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    print("Download complete... {}".format(filename))
    return filename