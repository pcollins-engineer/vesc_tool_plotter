import csv
import json
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .models import CsvRow
from .forms import FoilForm, BoardForm, MotorForm, PropellerForm, ControllerForm, RideForm, BuildForm

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

    if request.user.is_authenticated:
        if request.method == 'POST':
            print("ride here")
            rideForm = RideForm(request.POST, request.FILES)
            if rideForm.is_valid():
                rideForm.save()
                rideTitle = rideForm.cleaned_data.get('title')
                messages.success(request, 'Ride ' + rideTitle + ' was created')
                handle_uploaded_file(request.FILES["file"])

    return render(request, "plotter/upload.html", context={'accepted_data_set':ACCEPTED_DATA_SET, 'rideForm': rideForm })

def graph(request):
    send_data = parse_file(request)
    return render(request, "plotter/graph.html", context={"mydata": send_data})

def profile(request):
    return render(request, "plotter/profile.html", {})

def add_build(request):
    boardForm = BoardForm()
    foilForm = FoilForm()
    motorForm = MotorForm()
    propellerForm = PropellerForm()
    controllerForm = ControllerForm()
    return render(request, "plotter/add_build.html", context={'boardForm':boardForm, 'foilForm':foilForm, 'motorForm':motorForm, 'propellerForm':propellerForm, 'controllerForm':controllerForm})
