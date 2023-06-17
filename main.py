import playsound
import cv2
import uuid
import requests
import json
import easyocr
import pandas as pd

def start_again():
    cam_test()

def extract_numberplate(image):
    reader = easyocr.Reader(['en'])
    try:
        output = reader.readtext('/project/plates/'+image)
        numberplate=output[0][1]
        print(numberplate)
        return numberplate
    except IndexError as e:
            print("Image is not Clear")    
    except Exception as e:
            print(e)

    

def excel_sheet(numberplate):
    sheet_id = '1MkVBQYNqql8Ui7YScYl3IXQeRlHzaX1f9Z5CERndSME'
    df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv')

    if numberplate in df['Number Plate'].values:
        row = df[df['Number Plate'] == numberplate]
        bus_name = row.iloc[0, 1]
        place = row.iloc[0, 2]
        if bus_name == "Kee yeS aaR Tee see":
            print('\n\n\nBus Name: KSRTC')
        print('Destination: '+place)
        return bus_name,place
    else:
        print("The Number Plate is not registered ")
        return 0
    

def generate_sound(place,bus_name):

    url = 'http://3.111.82.58:8080/text'
    str= place+' bhaagatthekulla '+bus_name+' basu sttaandil etthi chernnirikkunnu'
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
    file_name=uuid.uuid4().hex
    if response.status_code == 200:
        audio_content = audio_file.content
        with open(file_name+'.wav', 'wb') as f:
            f.write(audio_content)
            print('File name: '+file_name+'.wav')
    else:
        print('Error: Failed to download file.')
    playsound.playsound('prefix.mp3')
    try:
        playsound.playsound(file_name+'.wav')
    except playsound.PlaysoundException as e:
        print(e)
    
    return 1


def cam_test():
    harcascade = "model/haarcascade_russian_plate_number.xml"
    # link= 'http://192.168.137.134:1100/video'
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)
    min_area = 500
    count = 0
    destroy =1
    completed = 0
    img_roi = 0

    while not completed:
        success, img = cap.read()
        sound =0
        plate_cascade = cv2.CascadeClassifier(harcascade)
        img_gray = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)

        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        for (x,y,w,h) in plates:
            area = w * h

            if area > min_area:
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

                img_roi = img[y: y+h, x:x+w]
                cv2.imshow("Number Plates", img_roi)
                if count<20:
                    if img_roi.all != 0:
                        cv2.imwrite("plates/img" + str(count) + ".png", img_roi)
                        count+=1
                        # print(count)
                        img_roi = None

        if destroy:
            cv2.imshow("Result", img)
        if count ==20:
            cv2.destroyAllWindows()
            destroy=0
        if cv2.waitKey(1) & 0xFF == ord('c'):
                cv2.destroyAllWindows()
                print("\nProgram Terminated Succesfully...\n")
                exit()
        if count==20:
                cv2.destroyAllWindows()
                destroy=0
                print("\n20 Images are Captured: ✔\n")
        i=19
        while not destroy:
            if i> 0:
                number_plate=extract_numberplate('img'+str(i)+'.png')
                bus_info=excel_sheet(str(number_plate))
                if(bus_info!=0):
                    sound = generate_sound(bus_info[1],bus_info[0])
                i-=1
                if(i==0):
                    start_again()

                if(sound == 1):
                    print('Audio Played: ✔')
                    completed = 1
                    start_again()
                    
if __name__ == '__main__':
    cam_test()                
        