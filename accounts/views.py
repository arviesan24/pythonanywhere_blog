from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm  #import classes from the forms.py file

# Create your views here.

def login_view(request):
    print(request.user.is_authenticated())
    next = request.GET.get("next")
    title = "Login"
    form = UserLoginForm(request.POST or None)  #will get the value of form from forms.py via POST if not empty
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password) #get user info base on the login
        login(request,user)     #login base on the authentication
        if next:
            return redirect(next)  #if login was triggered by action which required login(ex. delete comment)
        return redirect("/")  #redirect to home page
    return render(request,"form.html", {"form":form, "title": title})

def register_view(request):
    next = request.GET.get("next")
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        login(request,user)
        if next:
            return redirect(next)  #if register was triggered by action which required login(ex. delete comment)
        return redirect("/")  # else just redirect to home page

    context = {
        "form": form,
        "title": title,

    }
    return render(request,"form.html", context)

def logout_view(request):
    logout(request)
    return redirect("/")  # redirect to home page

