import logging
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import MarksheetForm
from .models import Marksheet
from .utility.DataValidator import DataValidator

logger = logging.getLogger(__name__)


def validate(request):
    input_errors = {}
    input_errors['error'] = False
    if (DataValidator.isNull(request.POST["userName"])):
        input_errors['userName'] = 'user name is required'
        input_errors['error'] = True
    if (DataValidator.isNull(request.POST["firstName"])):
        input_errors['firstName'] = 'first name is required'
        input_errors['error'] = True
    if (DataValidator.isNull(request.POST["lastName"])):
        input_errors['lastName'] = 'last name is required'
        input_errors['error'] = True
    if (DataValidator.isNull(request.POST["email"])):
        input_errors['email'] = 'email is required'
        input_errors['error'] = True
    if (DataValidator.isNull(request.POST["password"])):
        input_errors['password'] = 'password is required'
        input_errors['error'] = True
    # elif (DataValidator.isPassword(request.POST["password"])):
    #     input_errors['password'] = 'password must contains Password123!'
    #     input_errors['error'] = True
    return input_errors


def user_signup(request):
    input_errors = {}
    if request.method == "POST":
        userName = request.POST["userName"]
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        email = request.POST["email"]
        password = request.POST["password"]
        print("Form data Received")
        input_errors = validate(request)
        if not input_errors['error']:
            obj = User.objects.create_superuser(userName, email, password)
            obj.first_name = firstName
            obj.last_name = lastName
            obj.save()
    return render(request, "Registration.html", {"inputerror": input_errors})


def user_signin(request):
    message = ''
    if request.method == "POST":
        # get the UserData from Form
        userName = request.POST["userName"]
        password = request.POST["password"]
        user = authenticate(username=userName, password=password)
        if user is not None:
            request.session["userName"] = userName
            login(request, user)
            return redirect("/ORS/welcome")
        else:
            message = "Invalid User"
    return render(request, "Login.html", {'message': message})


def welcome(request):
    return render(request, "Welcome.html")


def destroy(request):
    logout(request)
    return redirect("SIGN_IN")


@login_required()
def add_marksheet(request):
    message = ""
    form = MarksheetForm()
    if request.method == "POST":
        form = MarksheetForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Marksheet Added Successfully"
    return render(request, "Marksheet.html", context={"form": form, 'message': message})


@login_required()
def getAll_marksheet(request):
    objects = Marksheet.objects.all()
    return render(request, "MarksheetList.html", {"data": objects})


@login_required()
def edit_marksheet(request, id):
    message = ''
    obj = Marksheet.objects.get(id=id)
    form = MarksheetForm(instance=obj)
    if request.method == "POST":
        form = MarksheetForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            message = "Marksheet Updated Successfully"
    return render(request, "Marksheet.html", {"form": form, "id": id, 'message': message})


@login_required()
def delete_marksheet(request, id):
    obj = Marksheet.objects.get(id=id)
    obj.delete()
    return redirect("/ORS/list")


def test_logging(request):
    try:
        c = 10 / 0
    except Exception as e:
        logger.info(e)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.fatal("fatal message")
    return HttpResponse('<h1>Looger Works..!!!</h1>');
