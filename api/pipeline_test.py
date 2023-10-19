from .classes import InputProcessor, Pulze, DeepGram, Labs11


def run_pipeline(username: str, filename: str):
    """
    Runs through the entire pipeline, from uploading an audio file, processing it, generating a better script,
    displaying the tips, and playing new audio generated by 11labs.

    Audio -> InputProcessor -> DeepGram -> Pulze -> Labs11
    """
    pul = Pulze()
    dee = DeepGram()
    lab = Labs11(username)

    audio_file, _ = InputProcessor.process_input(filename)
    transcription, length = dee.transcribe(audio_file)

    audience = input("What audience is this presentation for: ")

    pul.configure_initial_prompts(audience)
    feedback, new_script = pul.generate_feedback(transcription, length)
    print(feedback)
    print(new_script)

    lab.generate_custom_response(audio_file, new_script)


if __name__ == "__main__":
    un = "TedTeam"
    tf = 'TARGET_AUDIO.mp3'
    run_pipeline(un, tf)
