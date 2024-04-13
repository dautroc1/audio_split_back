from flask import Flask, request, jsonify
import base64
import glob
import yt_dlp 
import os
import requests
import json
import base64
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    
    youtube_url = request.json.get('youtube_url')
    print(youtube_url)
    headers = {
    'content-length':'5292281',
    'sec-ch-ua':'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'accept':'application/json, text/javascript, */*; q=0.01',

    'x-requested-with':'XMLHttpRequest',
    'sec-ch-ua-mobile':'?0',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua-platform':'"Windows"',
    'origin':'https://aivocalremover.com',
    'sec-fetch-site':'same-origin',
    'sec-fetch-mode':'cors',
    'sec-fetch-dest':'empty',
    'referer':'https://aivocalremover.com/',
    'accept-encoding':'gzip, deflate, br, zstd',
    'accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cookie':'JSESSIONID=DE0F18A219F735E856E1CF563FEB2E5B; _ga_LVPSJYM5SL=GS1.1.1712902939.1.0.1712902939.0.0.0; _ga=GA1.2.715018779.1712902939; _gid=GA1.2.721360766.1712902940; dom3ic8zudi28v8lr6fgphwffqoz0j6c=ee3c4b1d-6c3d-4a9a-9a89-d5e8f7e18d25%3A2%3A1; sb_main_c83ab685e09c8fa6e7de3ac1a0604dff=1; sb_count_c83ab685e09c8fa6e7de3ac1a0604dff=1'}

     # client to many multimedia portals

    # downloads yt_url to the same directory from which the script runs
    def download_audio(yt_url):
        ydl_opts = {
            'format': 'worstaudio/worst',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([yt_url])
    def newest_mp3_filename():
        # lists all mp3s in local directory
        list_of_mp3s = glob.glob('./*.mp3')
        # returns mp3 with highest timestamp value
        return max(list_of_mp3s, key = os.path.getctime)

    download_audio(youtube_url)
    newest_mp3_path = os.path.join(os.getcwd(), newest_mp3_filename())
    print(newest_mp3_path)

        
    file_path = newest_mp3_filename()
    print(os.path.basename(file_path).encode('utf-8'))

    with open(file_path, 'rb') as audio_file:
        audio_content = audio_file.read()
    header = b'Content-Disposition: form-data; name="fileName"; filename="vocals.mp3"'
    header += b'Content-Type: audio/mpeg\r\n\r\n'
    audio_content1 = header + audio_content
    # Encode the audio content in base64
    audio_base64 = base64.b64encode(open(file_path, "rb").read())

    with open(file_path, 'rb') as file:
        file_content = file.read()
    file_name = os.path.basename(file_path).encode('utf-8')
    # Create a dictionary representing FormData-like object
    fd = {'fileName':(file_name,audio_content1)}
    #fd = {'xyz':audio_content1}

    response0 = requests.request("POST", "https://aivocalremover.com/api/v2/FileUpload", headers=headers, files=fd)
    print(response0.content)
    headers = {
    'content-length':'159',
    'sec-ch-ua':'"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'accept':'*/*',
    'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
    'x-requested-with':'XMLHttpRequest',
    'sec-ch-ua-mobile':'?0',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua-platform':'"Windows"',
    'origin':'https://aivocalremover.com',
    'sec-fetch-site':'same-origin',
    'sec-fetch-mode':'cors',
    'sec-fetch-dest':'empty',
    'referer':'https://aivocalremover.com/',
    'accept-encoding':'gzip, deflate, br, zstd',
    'accept-language':'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'cookie':'JSESSIONID=DE0F18A219F735E856E1CF563FEB2E5B; _ga_LVPSJYM5SL=GS1.1.1712902939.1.0.1712902939.0.0.0; _ga=GA1.2.715018779.1712902939; _gid=GA1.2.721360766.1712902940; dom3ic8zudi28v8lr6fgphwffqoz0j6c=ee3c4b1d-6c3d-4a9a-9a89-d5e8f7e18d25%3A2%3A1; sb_main_c83ab685e09c8fa6e7de3ac1a0604dff=1; sb_count_c83ab685e09c8fa6e7de3ac1a0604dff=1'}
    response_dict = json.loads(response0.text)
    print(response_dict)
    filename = bytes(response_dict['file_name'], 'utf-8')
    payload = b'file_name=' + filename + b'&action=watermark_video&key=X9QXlU9PaCqGWpnP1Q4IzgXoKinMsKvMuMn3RYXnKHFqju8VfScRmLnIGQsJBnbZFdcKyzeCDOcnJ3StBmtT9nDEXJn&web=web'
    response1 = requests.request("POST", "https://aivocalremover.com/api/v2/ProcessFile", headers=headers, data=payload)
    print(response1.content)
    response_dict = json.loads(response1.text)
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
        print("File deleted successfully.")
    else:
        print("The file does not exist.")
    return {'message': 'URL processed successfully', 'vocal_path': response_dict['vocal_path'], 'instrumental_path': response_dict['instrumental_path'] }, 200
if __name__ == '__main__':
    # Use Gunicorn or uWSGI to run the Flask app in production
    app.run(host='0.0.0.0', port=5000)