from django.shortcuts import render, get_object_or_404, redirect
from .models import Classroom, Status, Bulb
import requests
import threading

Userver = "blr1.blynk.cloud"

def fetch_status(status, status_data):
    url = f"https://{Userver}/external/api/get?token={status.token}&pin={status.pin}"
    response = requests.get(url)
    fetched_status = response.text
    status_data.append({'id': status.id, 'status': fetched_status})

    # Update the status in the database
    status.status = fetched_status
    status.save()

def index(request):
    classrooms = Classroom.objects.all()
    status_data = []

    threads = []
    for classroom in classrooms:
        statuss = Status.objects.filter(classroom=classroom)

        for sts in statuss:
            thread = threading.Thread(target=fetch_status, args=(sts, status_data))
            thread.start()
            threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    context = {
        'classrooms': classrooms,
        'status_data': status_data
    }

    return render(request, 'index.html', context)

# Rest of the code remains the same...



def update_pin(request, bulb_id):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        status = request.POST.get('status')
        token = request.POST.get('token')

        # Update the bulb status
        bulb = get_object_or_404(Bulb, id=bulb_id)
        bulb.status = 1 if status.lower() == 'on' else 0
        bulb.save()

        # Send API request to update the physical bulb
        url = f"https://{Userver}/external/api/update?token={token}&{pin}={bulb.status}"
        requests.get(url)
        print(url)

    return redirect('/')