import easyocr
def extract_numberplate(image):
    reader = easyocr.Reader(['en'])
    try:
        output = reader.readtext('/project/plates1/'+image)
        numberplate=output[0][1]
        print(numberplate)
        return numberplate
    except IndexError as e:
            print("Image is not Clear")
    except Exception as e:
            print(e)
            

extract_numberplate('img0.png')