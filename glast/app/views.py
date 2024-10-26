from django.shortcuts import render

from .forms import UserRegistration,Homeform
from .models import *


def index(request):
    UserAlreadyExist=None
    fm=UserRegistration()
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        objects = Users.objects.filter(username=username).first()
        if objects:
            return render(request, 'index.html',{"form":fm,"UserAlreadyExist":"Username already exist"})
        else:
            object_created=Users.objects.create(username=username,password=password)
            if object_created:
                homeform=Homeform()
                print("object Created...",object_created)
                return render(request, 'home.html',{"homeform":homeform})
            
    return render(request, 'index.html',{"form":fm,"UserAlreadyExist":UserAlreadyExist})

def home(request,error=None):
    homeform=Homeform()
    if error:
        return render(request, 'home.html',{"homeform":homeform, 'error_msg':error})   
    else:
        return render(request, 'home.html',{"homeform":homeform})   
    
def game(request):
    print("The request object...",request)
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        group_name=request.POST['groupname']
        print("details....",username,password,group_name)
        return render(request, 'game.html',{'user_name':username,'password':password,'group_name':group_name})

    return render(request, 'game.html',{'user_name':None,'password':None,'group_name':None})

