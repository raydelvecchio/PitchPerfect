import requests
import os
from dotenv import load_dotenv
load_dotenv('../.env')


class Labs11:
    def __init__(self):
        self.key = os.environ['11labs_Key']

    def __create_new_voice(self, audio_file: str) -> str:
        """
        Given an audio file, create a new voice in 11labs and return the voice ID.
        """
        url = "https://api.elevenlabs.io/v1/voices/add"

        headers = {
            "Accept": "application/json",
            "xi-api-key": f"{self.key}"
        }

        data = {
            'name': 'Test_Voice',
            'labels': '{"accent": "American"}',
            'description': 'Test voice for Ted AI hackathon.'
        }

        files = [
            ('files', (audio_file, open(audio_file, 'rb'), 'audio/mpeg')),
        ]

        response = requests.post(url, headers=headers, data=data, files=files)
        return response.json()['voice_id']

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
        with open('output.mp3', 'wb') as f:
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
        labs = Labs11()
        labs.generate_custom_response(audio_file, script)

    test_11labs()
