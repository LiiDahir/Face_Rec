from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from django.http import JsonResponse
from django.contrib.auth import logout
from django.utils.decorators import decorator_from_middleware
from Group76.middleware import NoCacheMiddleware
import os
pathka = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from .main import *
from .xog import *
from .models import *
db.create_user()
obj=Main()
# Create your views here.
def login(request):
    # return HttpResponse(pathka)
    return render(request,"login.html",{"user":""})
def check(request):
    if request.method == "POST":
        user = request.POST ["user"]
        Pass = request.POST ["pass"]
        userka = db.get_user(user)
        try:
            if user == userka[0] and Pass == userka[3]:
                request.session["user"] = userka[0] 
                request.session["type"] = userka[2]
                 
                return render(request,"index.html",{"users":db.get_users(),"students":db.get_students()})
            else:
                userka = "User or Password is incorrect"
        except:
            userka = "This User user is not exsits"
    return render(request,"login.html",{"user":userka})
def edit(request,id):
    if request.method == "POST":
        user = request.POST ["user"]
        Pass = request.POST ["pass"]
        gmai = request.POST ["gmail"]
        user_type = request.POST ["type"]
        if gmai[-10:] == "@gmail.com":
            db.delete_user(id)
            x = db.insert_user(user,gmai,user_type,Pass)
            if x == None:
                return render(request,"signup.html",{"fill":[""], "users":db.get_users()})
            else:
                return render(request,"signup.html",{"erorr":x ,"users":db.get_users()})

        else:
            return render(request,"signup.html",{"eror":"invalid gmail","users":db.get_users()})
    else:redirect()

    userka = db.get_user(id)
    uses = db.get_users()
    return render(request,"signup.html",{"fill":userka,"user":uses})
def save(request):
    if request.method == "POST":
        user = request.POST ["user"]
        Pass = request.POST ["pass"]
        gmai = request.POST ["gmail"]
        user_type = request.POST ["type"]
        if gmai[-10:] == "@gmail.com":
            x = db.insert_user(user,gmai,user_type,Pass)
            if x == None:
                return render(request,"signup.html",{"fill":[""], "users":db.get_users()})
            else:
                return render(request,"signup.html",{"erorr":x ,"users":db.get_users()})

        else:
            return render(request,"signup.html",{"eror":"invalid gmail","users":db.get_users()})

def index(request):
    return render(request,"index.html",{"students":db.get_students()})
def train(request):
    return render(request,"train.html",{"num_of_image":{"header":"","content":""},"info_of_image":{"dup_header":"","dup_content":"","remove_header":" ","rem_content":""}})
def test(request):
    return render(request,"test.html",{})
def signup(request):
    return render(request,"signup.html",{"fill":[""],"user":db.get_users()})


def logout(request):
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def rename(request):
    if request.method=="POST":
        try:
            for i in os.listdir(pathka + "/media/dataset/check/"):
                os.remove(pathka +"/media/dataset/check/"+i)
        except:
            pass
        images=request.FILES.getlist("Images")
        try:
            id = request.POST["ID"]
            Name = request.POST["Name"]
            Class = request.POST["Class"]
            Email = request.POST["Email"]
        except:
            id=""
        img=Images()
        for i in images:
            img.images=i
            img.save()
        num_of_files=obj.rename_files()
        num_of_files="number of Images of renamed are : "+str(num_of_files)
        if id != "":
            info_of_image=obj.generate([id,Name,Class,Email])
        else:
            info_of_image=obj.generate([])
    return render(request,"train.html",{"num_of_image":{"header":"renamed images","content":info_of_image[0]},"info_of_image":{"dup_header":"duplicated images and same person",
            "dup_content":info_of_image[1],"remove_header":"removed Image","rem_content":info_of_image[2]}})

def recognize_faces(request):
    List =[]
    sawir = ""
    if request.method=="POST":
        try:
            for i in os.listdir(pathka + "/media/dataset/check/"):
                os.remove(pathka + "/media/dataset/check/"+i)
        except:
            pass

        images=request.FILES.getlist("Images")
        img=Images()
        for i in images:
            img.images=i
            img.save()
        for i in os.listdir(pathka + "/media/dataset/check/"):
            sawir = i
            x=obj.recognize_face(pathka + "/media/dataset/check/"+i,distance_threshold=0.0)
            List.append(x)
        return render(request,"test.html",{"test_image":"/media/dataset/check/"+sawir,"data":List[0]})