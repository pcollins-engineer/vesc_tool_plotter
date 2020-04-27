from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
    return render(request, "index.html", {})

def upload(request):
    template_data = {}
    def handle_uploaded_file(f):
        with open("log.csv", "wb+") as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    handle_uploaded_file(request.FILES["log_file"])

    template_data["test"] = "hi"

    return render(request, "table.html", template_data)