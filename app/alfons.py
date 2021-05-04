import speech_recognition as sr # recognise speech
import os # to remove created audio files
#import playsound # to play an audio file
from gtts import gTTS # google text to speech
import time
import random
from functools import lru_cache
from flask import Flask, jsonify, request
from transformers import AutoModelForCausalLM, AutoTokenizer
from playsound import playsound
import torch

os.environ['KMP_DUPLICATE_LIB_OK']='True'
os.environ["TOKENIZERS_PARALLELISM"] = "false"

@lru_cache()
def load_model():
    recognizer = sr.Recognizer() # initialise a recogniser
    print("model was loaded")
    return recognizer

@lru_cache()
def load_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
    model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
    return tokenizer, model

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def main():
    if request.method == "POST":
        # we will get the question from the request
        mode = str(request.data).strip("b''")
        print("This is the mode in SR: ", mode)
        tokenizer, model = load_tokenizer()
        r = load_model()
        while mode == "activate":
            
            conversation(tokenizer, model, r)
        sr.close()
        return jsonify("deactivate")


def conversation(tokenizer, model, r):
    try:
        # Let's chat for 99999 lines
        for step in range(99999):
            # encode the new user input, add the eos_token and return a tensor in Pytorch
            new_user_input_ids = tokenizer.encode(speech_recognizer(tokenizer, model, r) + tokenizer.eos_token, return_tensors='pt')

            # append the new user input tokens to the chat history
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

            # generated a response while limiting the total chat history to 1000 tokens, 
            chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

            # pretty print last ouput tokens from bot
            print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
            speak(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))
    except sr.UnknownValueError:
        speak("What the hell?")
        conversation(tokenizer, model, r)

def speech_recognizer(tokenizer, model, r):
    # listen for audio and convert it to text:
    with sr.Microphone() as source: # microphone as source
        voice_data = ''
        init_question = ['How can I help you?', 'Hello there!', 'Do you have any questions?', 'Whhaazzzuuuuuuup?', 'Is there no one else?']
        speak(random.choice(init_question))
        audio = r.listen(source)  # listen for the audio via source
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
            print(f">> {voice_data.lower()}") # print what user said
            return voice_data.lower()
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
            conversation(tokenizer, model, r)
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
            conversation(tokenizer, model, r)
        print(f">> {voice_data.lower()}") # print what user said

# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save("../audio/"+ audio_file) # save as mp3
    playsound("../audio/"+ audio_file) # play the audio file
    print(f"alfons: {audio_string}") # print what app said
    os.remove("../audio/"+ audio_file) # remove audio file

if __name__ == "__main__":
    app.run()

# FLASK_ENV=development FLASK_APP=alfons.py flask run --port=5003