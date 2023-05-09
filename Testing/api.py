def generate_sound(place,bus_name):
    import requests
    import json
    from playsound import playsound
    import time

    url = 'http://3.111.82.58:8080/text'
    str= place+' bhaagatthekulla '+bus_name+' basu sttaandil etthi chernnirikunnu'
    post_data = {
        "text": str,
        "author": "aloyise"
    }
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(post_data), headers=headers)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        audio_url = response_data['src']
        print(audio_url)
    else:
        print("POST didnt worked")

    audio_file = requests.get(audio_url)
    if response.status_code == 200:
        audio_content = audio_file.content
        with open('audio.wav', 'wb') as f:
            f.write(audio_content)

        print('File saved successfully.')
    else:
        print('Error: Failed to download file.')
    time.sleep(5)
    playsound('prefix.mp3')
    #time.sleep(2)
    playsound('audio.wav')
    return 1

generate_sound('Kannooor','yessemmess')
