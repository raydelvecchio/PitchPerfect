import requests
from moviepy.editor import *
import re
import os
import json
from dotenv import load_dotenv
load_dotenv('.env')


class InputProcessor:
    def __init__(self):
        pass

    @staticmethod
    def process_video_input(filename: str) -> tuple[str, str]:
        """
        Given an input VIDEO file, split them up into their video and audio components. Returns a tuple of
        (audio file, video file).
        """
        name = re.sub(r'\..*$', '', filename)

        video = VideoFileClip(filename)

        audio = video.audio
        audio.write_audiofile(f'splits/{name}.mp3')

        video_without_audio = video.without_audio()
        video_without_audio.write_videofile(f'splits/{name}.mp4', audio_codec='none')

        audio.close()
        video.close()
        video_without_audio.close()

        return f'splits/{name}.mp3', f'splits/{name}.mp4'


class Labs11:
    def __init__(self, username, store_file='keystore.json'):
        self.store_file = store_file
        self.username = username
        self.key = os.environ['11labs_Key']
        if not os.path.exists(store_file):
            with open(store_file, "w") as file:
                json.dump({}, file, indent=4)

    def __create_new_voice(self, audio_file: str) -> str:
        """
        Given an audio file, create a new voice in 11labs and return the voice ID. First checks our datastore to
        ensure we aren't generating multiple audio voices in 11labs for each user.
        """
        with open(self.store_file, "r") as file:
            data = dict(json.load(file))
        if self.username in data:
            return data[self.username]

        url = "https://api.elevenlabs.io/v1/voices/add"
        headers = {
            "Accept": "application/json",
            "xi-api-key": f"{self.key}"
        }
        data = {
            'name': f"Username_{self.username}",
            'labels': '{"accent": "American"}',
            'description': 'Ted AI hackathon generated voice'
        }
        files = [
            ('files', (audio_file, open(audio_file, 'rb'), 'audio/mpeg')),
        ]
        response = requests.post(url, headers=headers, data=data, files=files)
        voice_id = response.json()['voice_id']

        # updating our user -> voice ID dictionary
        with open(self.store_file, "r") as file:
            data = json.load(file)
        data[self.username] = voice_id
        with open(self.store_file, "w") as file:
            json.dump(data, file, indent=4)

        return voice_id

    def __generate_audio(self, voice_id: str, script: str, chunk_size: int = 1024):
        """
        Given a voice ID and a script, generate an MP3 file of that voice saying the given script.
        """
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": f"{self.key}"
        }
        data = {
            "text": script,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.6,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=data, headers=headers)
        with open(f"audio_outputs/{self.username}_Output.mp3", 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

    def generate_custom_response(self, audio_file: str, script: str):
        """
        First creates a voice in 11labs with the given audio file, then speaks it with a script.
        """
        voice_id = self.__create_new_voice(audio_file)
        self.__generate_audio(voice_id, script)


if __name__ == "__main__":
    def test_11labs():
        script = "Today I will be pitching my startup Crux. Thank you! I love analyzing pitch decks."
        audio_file = "test_audio.mp3"
        username = "Ray"
        labs = Labs11(username)
        labs.generate_custom_response(audio_file, script)

    def test_input_processor():
        video_file = "Bad_Pitch.mov"
        InputProcessor.process_video_input(video_file)

    test_input_processor()
