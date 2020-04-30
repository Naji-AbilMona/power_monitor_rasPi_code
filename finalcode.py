# import the necesary packages
import PySimpleGUI as sg
import signal, os
import sys
#from picamera import Picamera
import picamera
from time import sleep
import numpy as np
from PIL import Image
from subprocess import call
from datetime import datetime
#import datetime
from datetime import date
from datetime import time
import requests
import pyrebase
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore, db
import os, io
from google.cloud import vision
from google.cloud.vision import types

#converting timestamp for better reads
def convert():
    year = str(datetime.now().year)
    month = str(datetime.now().month)
    if len(month) < 2:
        month = '0'+ month
    day = str(datetime.now().day)
    if len(day) < 2:
        day = '0' + day
    hour = str(datetime.now().hour)
    if len(hour) < 2:
        hour = '0' + hour
    minute = str(datetime.now().minute)
    if len(minute) < 2:
        minute = '0' + minute

    dT = year + month + day + hour + minute
    return dT


# firebase storage connection
config = {
    "apiKey": "AIzaSyBSHonsGPHDJ3B5Cg7nJJ0_AOmomYNiCOI",
    "authDomain": "power-monitor-889a4.firebaseapp.com",
    "databaseURL": "https://power-monitor-889a4.firebaseio.com",
    "projectId": "power-monitor-889a4",
    "storageBucket": "power-monitor-889a4.appspot.com",
    "messagingSenderId": "289418668812",
    "appId": "1:289418668812:web:643f794f7e284bcf197729",
    "measurementId": "G-96LQ8T56Q3"
}
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()




#google vision api
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] =r'/home/pi/final/visionApi.json'
client = vision.ImageAnnotatorClient()


def handler(signum, frame):
    print('error, no input detected. Please input your email', signum)
    #event, values = window.read()
    window.close()


# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGALRM, handler)
signal.alarm(40)

#def input():
sg.theme('TanBlue')
layout = [[sg.Text('Please input your email')],      
                 [sg.InputText(key='-IN-')],      
                 [sg.Submit(), sg.Cancel()]]      

window = sg.Window('Login window', layout)    

event, values = window.read(close=True)    

text_input = values['-IN-']
    #return login_id

signal.alarm(0)
if text_input == None:
    text_input = 'demo2@powermonitor.com'



#firestore connection
cred = credentials.Certificate('/home/pi/final/PW.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
s1= text_input
doc_ref = db.collection('consumption').document(s1.strip())


#part that takes pictures
filePath= "/home/pi/Desktop/testfiles/"
camera = picamera.PiCamera()

#adjust time between pics
betweenpictures=10800


#infinite loop
while True:
    #grab the current time
    currentTime = datetime.now()
    lastread = currentTime.strftime("%d/%m/%Y-%H:%M")
    #create file name for our project
    picTime = currentTime.strftime("%d.%m.%Y-%H%M%S")
    picName = picTime + '.jpg'
    completeFilePath = filePath + picName
    path_on_cloud= s1+"/"+picName
    path_local = completeFilePath
    #takepicture
    camera.capture(completeFilePath)
   
    #read picture content
    with io.open(os.path.join(filePath,picName),'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    text = [texts.description for texts in response.text_annotations]
    print(text)
   
    ######
    doc = doc_ref.get()
    odo = u'{}'.format(doc.to_dict()['odometer'])
    ######
   
   
    send = ''
   
    list = ['0','1','2','3','4','5','6','7','8','9']
    if text:
        for i in range(6):
            if text[0][i] in list:
               
                send += text[0][i]
            else:
                send +="0"
       
       
        if odo == '000000':
            send = send
        elif int(send) > int(odo)+10:
            temp = int(odo)+1
            send = str(temp)
           
        elif int(send) < int(odo):
            temp = int(odo)+1
            send = str(temp)
           
    else:
        temp = int(odo)+1
        send += str(temp)
        print('bad read')
    #print(send)
   
    #update firestore
    doc_ref.set({
    'historicReads': {convert():send}#{convert():ft[0]}#{convert():text[0]}#
    }, merge=True)

    doc_ref.update({
      'odometer': send,#ft[0],#
      'timeStamp': lastread,#firestore.SERVER_TIMESTAMP,
     })
   
    #save picture on firebase storage
    storage.child(path_on_cloud).put(path_local)

   
    #wait till next picture
    sleep(betweenpictures)