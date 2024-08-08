from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment
from .forms import AppointmentForm
from testapp.models import CustomUser 
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import json
from django.conf import settings
from google_auth_oauthlib.flow import Flow


CREDENTIALS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')
CLIENT_SECRET_FILE_PATH = os.path.join(os.path.dirname(__file__), 'client_secret.json')

def oauth2callback(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE_PATH,
        scopes=SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI
    )

    if 'code' not in request.GET:
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return redirect(authorization_url)
    
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    creds_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    with open(CREDENTIALS_FILE_PATH, 'w') as token:
        json.dump(creds_data, token)

    return redirect('book_appointment', doctor_id=request.session['doctor_id'])

def create_google_calendar_event(appointment):
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    if not os.path.exists(CREDENTIALS_FILE_PATH):
        raise FileNotFoundError("The credentials.json file is missing.")

    creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE_PATH, SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f'Appointment with Dr. {appointment.doctor.first_name} {appointment.doctor.last_name}',
        'start': {
            'dateTime': f'{appointment.date}T{appointment.start_time}',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': f'{appointment.date}T{appointment.end_time}',
            'timeZone': 'UTC',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, pk=doctor_id)  # Use CustomUser
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = request.user
            appointment.end_time = (datetime.combine(datetime.min, appointment.start_time) + timedelta(minutes=45)).time()
            appointment.save()

            try:
                create_google_calendar_event(appointment)
            except FileNotFoundError:
                request.session['doctor_id'] = doctor_id
                return redirect('oauth2callback')

            return redirect('appointment_details', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'appointment/book_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'appointment/appointment_details.html', {'appointment': appointment})



@login_required
def doctor_list(request):
    doctors = CustomUser.objects.filter(user_type='doctor')
    return render(request, 'appointment/doctor_list.html', {'doctors': doctors})



