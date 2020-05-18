import csv
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
<<<<<<< HEAD
from .models import CsvRow, Build, Ride, Foil, Board, Motor, Controller, Propeller
from .forms import FoilForm, BoardForm, MotorForm, PropellerForm, ControllerForm, RideForm, BuildForm
=======
from .models import CsvRow, Build, Ride
from .forms import FoilForm, BoardForm, MotorForm, PropellerForm, ControllerForm, RideForm, BuildForm, BuildSelectForm
>>>>>>> 7eafa6f23c4e9b315dd59432334ff45cdb4845e8

ACCEPTED_DATA_SET = {
    "temp_motor",
    "current_motor",
    "current_in",
    "d_axis_current",
    "q_axis_current",
    "erpm",
    "duty_cycle",
    "amp_hours_used",
    "amp_hours_charged",
    "watt_hours_used",
    "watt_hours_charged"
}

def handle_uploaded_file(f):
    with open("file.csv", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Not logged in
def parse_file(request):
    template_data = {}
    with open("file.csv") as f:
        reader = csv.reader(f, delimiter=";")
        dataMap = {}
        header = []
        for index, head in enumerate(next(reader)):
            #always append first element for time
            if index == 0:
                dataMap[index] = head
                header.append(head)
            if head in ACCEPTED_DATA_SET:
                dataMap[index] = head
                header.append(head)

        # O(nRows*mdataMapkeys)
        data = []
        for row in reader:
            rowData = []
            for key in dataMap:
                rowData.append(row[key])
            if request.user.is_authenticated:
                newRow = CsvRow()
                newRow.create_row()
            data.append(rowData)

        template_data = {
            "header": header,
            "data": data
        }
        send_data = json.dumps(template_data)
        return send_data

def upload(request):
    rideForm = RideForm()
    buildSelectForm = BuildSelectForm(request=request)

    if request.user.is_authenticated:
        if request.method == 'POST':
            print("ride here")
            rideForm = RideForm(request.POST, request.FILES)
            buildSelectForm = buildSelectForm(request.POST)
            if rideForm.is_valid():
                rideForm.save()
                rideTitle = rideForm.cleaned_data.get('title')
                messages.success(request, 'Ride ' + rideTitle + ' was created')
                handle_uploaded_file(request.FILES["file"])

    return render(request, "plotter/upload.html", context={'accepted_data_set':ACCEPTED_DATA_SET, 'rideForm': rideForm, 'buildSelectForm': buildSelectForm })

def graph(request):
    send_data = parse_file(request)
    return render(request, "plotter/graph.html", context={"mydata": send_data})

def profile(request, username):
    user_id = get_object_or_404(User, username=username).pk
    builds = Build.objects.filter(author=user_id)
    rides = Ride.objects.filter(rider=user_id)
    return render(request, "plotter/profile.html", context={"username": username, "builds":builds, "rides":rides})

@login_required(login_url='/login/')
def add_build(request):
    buildForm = BuildForm(prefix='build')
    boardForm = BoardForm(prefix='board')
    foilForm = FoilForm(prefix='foil')
    motorForm = MotorForm(prefix='motor')
    propellerForm = PropellerForm(prefix='propeller')
    controllerForm = ControllerForm(prefix='controller')

    if request.user.is_authenticated:
        if request.method == 'POST':
            buildForm = BuildForm(request.POST, prefix='build')
            boardForm = BoardForm(request.POST, prefix='board')
            foilForm = FoilForm(request.POST, prefix='foil')
            motorForm = MotorForm(request.POST, prefix='motor')
            propellerForm = PropellerForm(request.POST, prefix='propeller')
            controllerForm = ControllerForm(request.POST, prefix='controller')
            if buildForm.is_valid() and boardForm.is_valid() and foilForm.is_valid() and motorForm.is_valid() and propellerForm.is_valid() and controllerForm.is_valid():
                #get form object but dont save
                build = buildForm.save(commit=False)
                board = boardForm.save()
                foil = foilForm.save()
                motor = motorForm.save()
                prop = propellerForm.save()
                controller = controllerForm.save()
                # setting foreign keys
                build.author = request.user
                build.board = board
                build.foil = foil
                build.motor = motor
                build.propeller = prop
                build.controller = controller
                build.save()
                title = buildForm.cleaned_data.get('title')
                messages.success(request, 'Build "' + title + '" was created')
                return redirect('/build')

    return render(request, "plotter/add_build.html", context={'boardForm':boardForm, 'foilForm':foilForm, 'motorForm':motorForm, 'propellerForm':propellerForm, 'controllerForm':controllerForm, 'buildForm':buildForm})

def edit_build(request, username, build, form):
    build = get_object_or_404(Build, id=build.id)
    return render(request, "plotter/profile.html", {})
