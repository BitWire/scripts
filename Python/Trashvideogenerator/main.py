#!/usr/bin/env python3

import requests
import time
import pyttsx3
from moviepy.editor import *

# Get the data link of the subreddit config['subreddit']
link = 'https://www.reddit.com/r/' + 'AskReddit' + '/.json'


text = []

def checkRatelimit(headers):
    remaining = headers['x-ratelimit-remaining']
    used = headers['x-ratelimit-used']
    reset = headers['x-ratelimit-reset']

def getQuestions(post):
    redditThread = requests.get(post['url'] + '.json', headers={'User-agent': 'trashVideoGeneratorScript 0.1 (by /u/xxx)'})
    print(redditThread.headers['x-ratelimit-remaining'])
    if redditThread.status_code == 200:
        redditThreadJson = redditThread.json()
        comments = []
        comments.append(post['title'])
        for i in range(0, 2):
            comment = redditThreadJson[1]['data']['children'][i]['data']
            comments.append(comment['body'])
        return comments
    else:
        return ['StatusCode 429', 'Throttled']


def text2Speech(texts):
    i = 0
    engine = pyttsx3.init()
    for text in texts:
        for i in range(0, len(text)):
            fileName = 'text' + str(i) + '.mp3'
            engine.save_to_file(text[i], fileName)
            engine.runAndWait()
            engine.stop()
        i++1



def Speech2Video(texts):
    audio0 = AudioFileClip("text0.mp3", fps=44100).set_start(0)
    duration0 = audio0.duration + 2
    audio1 = AudioFileClip("text1.mp3", fps=44100).set_start(duration0)
    duration1 = duration0 + (audio1.duration + 2)
    audio2 = AudioFileClip("text2.mp3", fps=44100).set_start(duration1)
    final_audio_clip = CompositeAudioClip([audio0,audio1,audio2])        
    clip = VideoFileClip("subway-surfers.mp4").subclip(5,(final_audio_clip.duration + 7))
    clip = clip.set_audio(final_audio_clip)
    clip.write_videofile('test.avi', codec="mpeg4")


# Make the actual request to get the data
r = requests.get(link, headers={'User-agent': 'trashVideoGeneratorScript 0.1 (by /u/xxx)'})

# Get the json data from the request
json = r.json()

# Get a picture for every monitor
for i in range(0, 2):
    post = json['data']['children'][i]['data']
    if 'title' not in post or not post['title'].endswith('?'):
        continue
    text.append(getQuestions(post))
    print(text)
    text2Speech(text)
    Speech2Video(text)
quit()
