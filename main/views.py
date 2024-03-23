from django.shortcuts import render
import base64
import io
from PIL import Image
from django.http import HttpResponse
import cv2
import numpy
from main.process_img import decect_inattention
from django.views.decorators.csrf import csrf_exempt
from main.models import User, Timetable
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import os
import matplotlib.pyplot as plt
from django.utils import timezone


 

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def add_to_timetable():
    d = datetime.now(tz=timezone.utc)
    timetable_object = Timetable.objects.create(username = 'artur', subject = 'subject', datetime = d)
    timetable_object.save()


def create_keys():
    
    key_pair = RSA.generate(2048)
    private_key = open("privatekey.pem", "wb")
    private_key.write(key_pair.exportKey())
    
    public_key = open("public_key.pem", "wb")
    public_key.write(key_pair.publickey().exportKey())

    public_key.close()
    private_key.close()

def decrypt_message(enc, request):
    enc = base64.b64decode(enc)
    ip = get_client_ip(request)
    cipher = AES.new(aes_key[ip].encode('utf-8'), AES.MODE_CBC, iv[ip].encode('utf-8'))
    return cipher.decrypt(enc)

aes_key = {}
iv = {}
@csrf_exempt
def student_auth(request):
    ip = get_client_ip(request)
    if (request.method == 'POST' and request.headers['Type'] == 'id'):
        if(User.objects.filter(nr_matricol = request.body.decode())):
            f = open("public_key.pem", "r")
            return HttpResponse(f.read())
        else:
            return HttpResponse("User not found") 
    elif(request.method == 'POST' and request.headers['Type'] == 'aes_key'):
        data = request.body.decode()
        f = open('privatekey.pem','r')
        key = RSA.importKey(f.read())
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        decrypted_message = cipher.decrypt(b64decode(data))
        global aes_key
        aes_key[ip] = decrypted_message.decode()
        print('key')
        print(aes_key[ip])
        return HttpResponse("Key recieved")
         
    elif(request.method == 'POST' and request.headers['Type'] == 'iv'):
        data = request.body.decode()
        f = open('privatekey.pem','r')
        key = RSA.importKey(f.read())
        cipher = PKCS1_OAEP.new(key, hashAlgo=SHA256)
        decrypted_message = cipher.decrypt(b64decode(data))
        global iv
        iv[ip] = decrypted_message.decode()
        print('iv')
        print(iv[ip])
        return HttpResponse("Iv recieved") 
    else:
        return render(request, 'student_auth.html')




@csrf_exempt
def main(request):
    return render(request, 'main.html')  
@csrf_exempt
def index(request):
    return render(request, 'index.html')  
def get_request(request):
    return HttpResponse("Get request recieved!")

subject = ''
filename = ''
drowsiness = []
stop_session_flag = False
@csrf_exempt
def post_request(request):
    data = request.body
    data = decrypt_message(data, request)
    data= data.decode("utf-8", "ignore")
    z = data[data.find('/9'):]
    #im = Image.open(io.BytesIO(base64.b64decode(z))).save('images/result' + z.replace("/", "1" )[-10:] + '.jpg')
    im = Image.open(io.BytesIO(base64.b64decode(z)))
    np_array_img = numpy.array(im)
    cv_img = cv2.cvtColor(np_array_img, cv2.COLOR_RGB2BGR)
    if len(drowsiness) < 5:
        drowsiness.append(decect_inattention(cv_img))
    else:
        now = datetime.now()
        dt_string = now.strftime("%H:%M-")
        global subject, filename

        f = open("C:\DjangoProjects\mysite\\attentiveness\\" + subject + '\\' + filename, "a")
        f.write(dt_string)
        f.write(str(sum(drowsiness)/5))
        f.write('\n')
        drowsiness.clear() 

    if stop_session_flag == False:
        return HttpResponse("Post request recieved!")
    else:
        return HttpResponse("Stop session!")




def get_nearest_date(items):
    now = datetime.now(tz=timezone.utc)
    return min(items, key=lambda x: abs(x.datetime - now))


@csrf_exempt
def teacher_my_page(request):
    
    if (request.method == 'POST'):
        if(request.headers['type'] == 'subject'):
            global subject
            username = (request.user.username)
            classes = Timetable.objects.filter(username = username)
            clas = get_nearest_date(classes)
            subject = clas.subject
            try:
                os.mkdir("C:\DjangoProjects\mysite\\attentiveness\\" + subject)
            except FileExistsError:
                print("Dir found")

            global filename
            filename = str(datetime.now().strftime("%Y.%m.%d.%H"))
            return HttpResponse(str(subject)+" on "+ str(filename))
        elif (request.headers['type'] == 'stop_session'):
            global stop_session_flag
            print("Here")
            if request.body.decode() == 'true':
                stop_session_flag = True
            return HttpResponse("Session stopped!")

    else:
        return render(request, 'prof.html')
 


#run server command
#python manage.py runserver_plus 192.168.100.32:8080  --cert-file cert.pem --key-file key.pe


