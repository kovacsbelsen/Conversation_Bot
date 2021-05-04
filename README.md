# Alfons , the conversation bot

#### Natural language processing mini-project

* Alfons is the chatbot you never knew you needed. 
* Instead of typing, just ask your question using your microphone and Alfons will understand you and provide a verbal response. Sometimes very funny ones.
* All you need to do, is a wait bit, while Alfons prepares for the conversation at the very beginning.


# Team
* [Michal](https://github.com/MichalPodlaszuk)
* [Tobias](https://github.com/Tobias-GH-Schulz)
* [Bence](https://github.com/kovacsbelsen)

# Libraries used
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
* [Transformers](https://pypi.org/project/transformers/)
* [Google Text-to-Speech](https://pypi.org/project/gTTS/)
* [Playsound](https://pypi.org/project/playsound/)

# How?

* Alfons understand human speech via the SpeechRecognition Python library, for which we use "sr.Microphone() as source" for audio input, to detect speech.
* It is then processed into text and printed, by listening to the words, by using "r.recognize_google(audio)".
* The bot processes the information using pretrained DialoGPT models, "microsoft/DialoGPT-large" and generates a response.
* The response and the end result is then trasnferred to audio, by utilizing "gTTS(text=audio_string, lang='en')".
* This is all encompassed within a for loop, so the user can speak with Alfons as many times as they like.
* The app is ran by utilizing flask.
