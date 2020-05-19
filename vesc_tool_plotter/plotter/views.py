import csv
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from .models import CsvRow, Build, Ride, Foil, Board, Motor, Controller, Propeller
from .forms import FoilForm, BoardForm, MotorForm, PropellerForm, ControllerForm, RideForm, BuildForm

ACCEPTED_DATA_SET = {
    "ms_today",
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
def parse_file(request, ride_id):
    template_data = {}
    with open("file.csv") as f:
        reader = csv.reader(f, delimiter=";")
        dataMap = {}
        rowMap = {}
        counter = 0
        header = []
        for index, head in enumerate(next(reader)):
            if head in ACCEPTED_DATA_SET:
                dataMap[index] = head
                header.append(head)
                rowMap[head] = counter
                counter += 1

        print(rowMap)

        # O(nRows*mdataMapkeys)
        data = []
        for row in reader:
            rowData = []
            for key in dataMap:
                rowData.append(row[key])
            if request.user.is_authenticated:
                newRow = CsvRow()
                for field in ACCEPTED_DATA_SET:
                    if field in rowMap:
                        setattr(newRow, field, rowData[rowMap[field]])
                    else:
                        setattr(newRow, field, None)
                ride = Ride.objects.filter(id=ride_id)
                newRow.ride = ride[0]
                newRow.save()
            data.append(rowData)

        template_data = {
            "header": header,
            "data": data
        }
        send_data = json.dumps(template_data)
        return send_data

def upload(request):
    rideForm = RideForm()
    if request.user.is_authenticated:
        user_id = request.user.id
        rideForm.fields["build"].queryset = Build.objects.filter(author=user_id)
        if request.method == 'POST':
            rideForm = RideForm(request.POST)
            if rideForm.is_valid():
                rideInfo = rideForm.save()
                handle_uploaded_file(request.FILES["file"])
                parse_file(request, rideInfo.id)
                urlPath = "/graph/" + str(rideInfo.id) + "/"
                return redirect(urlPath)

    return render(request, "plotter/upload.html", context={'accepted_data_set':ACCEPTED_DATA_SET, 'rideForm': rideForm })

def graph(request, ride_id):

    header_list = [
    "ms_today",
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
    ]

    template_data = {}
    data = []
    csvData = CsvRow.objects.filter(ride=ride_id)

    for row in csvData:
        rowData = row.getAllFields()
        data.append(rowData)

    template_data = {
        "header": header_list,
        "data": data
    }

    send_data = json.dumps(template_data)

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
