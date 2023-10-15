# Crux (Ted AI Multimodal Hackathon 2023)
AI-assisted presentation preparation companion. Using DeepGram, Pulze, and ElevenLabs.

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