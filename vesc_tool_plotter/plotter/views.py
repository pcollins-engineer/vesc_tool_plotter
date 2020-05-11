import csv
from django.shortcuts import render, HttpResponse
import json

accepted_data_set = {
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

def upload(request):
    return render(request, "plotter/upload.html", context={'accepted_data_set':accepted_data_set})

def graph(request):
    template_data = {}

    def handle_uploaded_file(f):
        with open("log_file.csv", "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    handle_uploaded_file(request.FILES["log_file"])

    with open("log_file.csv") as f:
        reader = csv.reader(f, delimiter=";")
        dataMap = {}
        header = []
        for index, head in enumerate(next(reader)):
            #always append first element for time
            if index == 0:
                dataMap[index] = head
                header.append(head)
            if head in accepted_data_set:
                dataMap[index] = head
                header.append(head)

        # O(nRows*mdataMapkeys)
        data = []
        for row in reader:
            rowData = []
            for key in dataMap:
                rowData.append(row[key])
            print(rowData)
            data.append(rowData)

        # ************** original parsing code
        # header = next(reader)
        # data = []
        # for row in reader:
        #     data.append(rowData)
        template_data = {
            "header": header,
            "data": data
        }
        send_data = json.dumps(template_data)

    return render(request, "plotter/graph.html", context={"mydata": send_data})

def profile(request):
    return render(request, "plotter/profile.html", {})
