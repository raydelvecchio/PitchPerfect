# Crux (Ted AI Multimodal Hackathon 2023)
AI-assisted presentation preparation companion. Using DeepGram, Pulze, and ElevenLabs. Built at SHACK15 in San Francisco.

# Team
* Ray Del Vecchio: Backend / Integration Developer
* Ayssar A: Frontend Developer
* Paul Smith: Designer
* Kailash Ambwani: Machine Learning Engineer

# Motivation
Many people, ourselves included, start out with minimal public speaking skills. Our cadence is off, our timing is wrong, we don't know how to emphasize key points, maybe we can't even articulate our information well at all. 

Current solutions focus on important style, mannerisms, speech, and body language, but they miss the larger point: getting the right message across, in the right way, to the right audience: this is the Crux of the matter!

Our solution coaches you to make your presentation get to the crux clearly and with great style. It takes a recording/video of a user's presentation, detects their word timing/cadence, physical expressions and postures. It also learns where the crux of the presentation is. It then provides constructive feedback on how to improve both their content and delivery so that the crux is optimally communicated, making the entire presentation more successful. But it's not just a static list of tactics. We generate a new script based on this feedback, and play it to the user in their OWN voice, showing them their true potential to live up to. With this iterative process, users can hone their performance as much as they want, helping them learn and improve communication skills.

# Pipeline
1. User prompted to record a pitch (audio, video, or both).
2. Pitch recording sent to our backend API.
3. API detects patterns in speech and video, including pitch content, timing, cadence, posture, gestures, and more.
4. Suggestions are generated with Pulze on how to improve *all aspects* of this pitch, using these patterns as input.
5. Suggestions displayed to the user.
6. Pulze uses its *own* suggestions to iteratively improve the pitch, generating a NEW script of equal length.
7. This new script is displayed to the user.
8. With 11labs, the script is read in the user's **own** voice, then played in the application for the user to 
hear how to pitch it themselves. 

# Run Instructions
* `pip install -r requirements.txt`
* To run the pipeline locally, run `pipeline_test.py`
* To activate the suggestions API, run `api.py`