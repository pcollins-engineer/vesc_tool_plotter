import csv
from django.shortcuts import render, HttpResponse
import json

# Create your views here.

def index(request):
    return render(request, "index.html", {})

def upload(request):
    template_data = {}
    def handle_uploaded_file(f):
        with open("log_file.csv", "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    handle_uploaded_file(request.FILES["log_file"])
    with open("log_file.csv") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
        data = []
        for row in reader:
            data.append(row)
        template_data = {
            "header": header,
            "data": data
        }
        send_data = json.dumps(template_data)
    return render(request, "table.html", context={"mydata": send_data})