#This script allows you to ask OpenAI Vision API
#questions about an item you show it
#The response is just in text in the terminal

import cv2
from openai import OpenAI
import os
import base64
import requests
from gtts import gTTS

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
    query = f'{query} - dont mention the hand holding the object'
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

os.system('clear')
while True:
    query = input('Your request: ')
    os.system('clear')
    take_pic(query)
