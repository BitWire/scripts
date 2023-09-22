import requests, sys, subprocess

# Needs playerctl installed on host system
title = str(subprocess.run(['playerctl', 'metadata', 'title'], capture_output=True, text=True).stdout)
artist = str(subprocess.run(['playerctl', 'metadata', 'artist'], capture_output=True, text=True).stdout)
text = title + ' - ' + artist
text = text.replace("\n", "")
print(text)
try:
    # This request is for sending data to an Awtrix compatible clock.
    # For more info see https://github.com/Blueforcer/awtrix-light
    requests.post('http://IP.OF.YOUR.CLOCK/api/custom?name=Devfreund', json={
        "text": text,
        "rainbow": False,
        "duration": 10,
        "icon": "EQ"
    })
except requests.exceptions.RequestException as e:
    print(e)