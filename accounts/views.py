from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.forms import RegisterForm
from django_email_verification import sendConfirm
from django.contrib.auth import get_user_model

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data["email"]
            user =  User.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'], password=form.cleaned_data['password1'], email=email)
            user.is_active = True
            user.save()
            login(request, user)
            #Uncomment sendConfirm and return for email verification also set user.is_active to False
            #sendConfirm(user)
            #return redirect("/accounts/confirm-email")
            return redirect("/home")
        else:
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("/accounts/signup")
    else:
        return render(request, "accounts/signup.html")

def login_view(request):

    # if request.user.is_authenticated:
    #     return redirect("/home")
    # if request.method == "POST":
    #     form = AuthenticationForm(data=request.POST)
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         if user.is_active == False:
    #             return redirect("/accounts/confirm-email")
    #         if "next" in request.POST:
    #             return redirect("/home")
    #         else:
    #             return redirect("/home")
    #     else:
    #         messages.error(request, 'Invalid Username/Password!')
    # else:
    form = AuthenticationForm()

    return render(request, "accounts/login_base.html", { "form": form })


def logout_view(request):
    logout(request)
    return redirect("/accounts/login")

def confirm_email(request):
    return render(request, 'confirm_email.html')
