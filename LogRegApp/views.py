import email
from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Users
import bcrypt

# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method =='POST':
        errors=Users.objects.validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
               messages.error(request, value)
            return redirect('/')
        else:
            fname=request.POST['fname']
            lname=request.POST['lname']
            email=request.POST['email']
            password=request.POST['password']
            pwHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

            newUser=Users.objects.create(fname=fname,lname=lname,email=email,password=pwHash)
            newUser.save()
            request.session['loggedInUser']=newUser.id
            return redirect("/success")  
    else:
        return redirect('/')             

def login(request):
    if request.method =='POST':
        users=Users.objects.filter(email=request.POST['email'])
        if len(users)==1:
            if not bcrypt.checkpw(request.POST['password'].encode(),users[0].password.encode()):
                messages.error(request,"Passwords dont match")
                return redirect('/')
            else:
                request.session['loggedInUser'] = users[0].id
                return redirect("/success")
        else:
            messages.error(request,"Email dose not exist")
    return redirect('/')                

def success(request):
    if not 'loggedInUser' in request.session:
        return redirect('/')
    else:    
        context = {
           'user':Users.objects.get(id=request.session['loggedInUser'])
        }
        return render(request,'success.html',context)


def logout(request):
    request.session.clear()
    return redirect('/')