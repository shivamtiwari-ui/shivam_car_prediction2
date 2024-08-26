from django.http import HttpResponse
from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def Home(request):
    return render (request, "index.html")



def carvaluation(request):
    return render(request,"carvaluation.html")




def emicalculator(request):
    return render (request , "emicalc.html")



def challan(request):
    return render (request , "challan.html")


def blog(request):
    return render(request , "blog.html")



def delhi(request):
    return render(request , "delhi.html")


def mumbai(request):
    return render(request , "mumbai.html")


def banglore(request):
    return render(request , "banglore.html")


def ahemdabad(request):
    return render(request , "ahemdabad.html")


def surat(request):
    return render(request , "surat.html")



def loan(request):
    return render(request , "loan.html")





# @login_required(login_url='login')
