# Made by: Rowan Ashraf
# For English press 'e'
# For Arabic press 'a'
# To quit press 'q'

import cv2
import numpy as np
import easyocr
import os
import gtts


def imageData(result, frame):
    "Function that takes the result from easyocr and frame, displays it, and converts text to speech"
    towrite = []
    for (bbox, text, prob) in result:
        if prob >= 0.4:
            # Displays text and probability of
            print(f'Detected text: {text} (Probability: {prob:.2f})')
            # Gets top-left and bottom-right bbox vertices
            (top_left, top_right, bottom_right, bottom_left) = bbox

            top_left = (int(top_left[0]), int(top_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

            # Creates a rectangle for bbox display
            cv2.rectangle(frame, pt1=top_left, pt2=bottom_right, color=(255, 0, 0), thickness=2)

            # put recognized text
            cv2.putText(frame, text=text, org=(top_left[0] + 5, top_left[1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.9, color=(0, 0, 0), thickness=4)

            # Appends text in a list to convert it to speech later
            towrite.append(text)

    # Convert text in the frame to speech
    if towrite != []:
        cv2.imshow("frame", frame)
        txtToSpeech(towrite)

def txtToSpeech(text):
    global language
    speech = ''
    for n in range(len(text)):
        speech = speech + ' ' + text[n]

    sound = gtts.gTTS(text=speech, lang=language, slow=False)

    # Saving the converted audio in a mp3 file
    sound.save("text.mp3")

    # Playing the converted file
    os.system("text.mp3")
    length = len(speech)
    cv2.waitKey(length*150)


language = 'en'

cap = cv2.VideoCapture(1)
reader = easyocr.Reader(['en'])
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        result = reader.readtext(frame)
        # print(result)

        # Displays all the visual and verbal data
        imageData(result, frame)

        k = cv2.waitKey(1)
        if k == ord('a'):
            reader = easyocr.Reader(['ar'])
            language = 'ar'
            print("Arabic mode")
        if k == ord('e'):
            reader = easyocr.Reader(['en'])
            language = 'en'
            print("English mode")
        if k == ord('q'):
            break
cv2.destroyAllWindows()
cap.release()
