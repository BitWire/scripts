import asyncio, requests, time
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

async def get_media_info():
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:  # there needs to be a media session running
        info = await current_session.try_get_media_properties_async()

        # song_attr[0] != '_' ignores system attributes
        info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

        # converts winrt vector to list
        info_dict['genres'] = list(info_dict['genres'])

        return info_dict

if __name__ == '__main__':
    while True:
        current_media_info = asyncio.run(get_media_info())
        text = str(current_media_info['title'] + ' - ' + current_media_info['artist'])
        try:
            # This request is for sending data to an Awtrix compatible clock.
            # For more info see https://github.com/Blueforcer/awtrix-light
            requests.post('http://IP.OF.YOUR.CLOCK/api/custom?name=Music', json={
                "text": text,
                "rainbow": False,
                "duration": 10,
                "icon": "EQ"
            })
        except requests.exceptions.RequestException as e:
            print(e)

        time.sleep(10)