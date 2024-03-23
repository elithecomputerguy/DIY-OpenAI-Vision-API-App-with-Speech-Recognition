#This script allows you to verbally ask OpenAI Vision API about an item you show it
#The trigger word is "computer"
#The response is turned into an .mp3 and played

import cv2
from openai import OpenAI
import os
import base64
import requests
from gtts import gTTS
import speech_recognition as sr
import time

current_directory = os.path.dirname(os.path.abspath(__file__))

#OpenAI Settings
api_key = 'APIKEY'
client = OpenAI(api_key=api_key)

#Encode Image in base64
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

#Upload and Process Image
def image_process(image_path, query):
    #query = 'what is this? answer in less than 20 words'
    query = f'''{query}\n
                - dont mention the hand holding the object \n
                - be succinct in your reponse
            '''
    print(f'Query: {query}')
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 300
        }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response = response.json()
    response = response['choices'][0]['message']['content']

    return response

#Take Picture from Webcam with OpenCV
def take_pic(query):
    image_name = 'what-is.png'
    image_path = os.path.join(current_directory, image_name)

    cam_port = 0
    cam = cv2.VideoCapture(cam_port) 

    result, image = cam.read() 

    if result: 
        cv2.imwrite(image_path, image) 
        response = image_process(image_path, query)

    else: 
        print("No image detected. Please! try again") 
        
    print(response)

    tts = gTTS(response, lang='en')
    tts.save('what-is.mp3')
    #Play the mp3 file. I use afplay for my Mac, for Ubuntu install and use mpg321
    os.system('afplay what-is.mp3')

#Speech to Text
def stt():
    query = ''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio).lower()
        print(f'Query: {query}')
    except sr.UnknownValueError:
        print("Google Speech Services - Unknown Error")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))    

    return query

os.system('clear')
#Continuous Loop to Listen for User Input. 
#"Computer" is used as the trigger word
while True:
    query = stt()
    os.system('clear')
    if 'computer' in query:
        take_pic(query)
    else:
        print(query)
        time.sleep(1)