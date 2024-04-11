from django.shortcuts import render, redirect
from App.models import Booking, Court, Image
from .forms import BookCourtForm
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def home(request):
   courts = Court.objects.filter(is_available=True)
#    images = Image.objects.all();
   context = {'courts': courts}
   return render(request, 'home.html', context)

def court(request, pk):
   form = BookCourtForm()
   court = Court.objects.get(id=pk)
   
   images = Image.objects.filter(court_id=pk)
   if request.method == 'POST':
      form = BookCourtForm(request.POST)
      if form.is_valid():
         with transaction.atomic():
            booking = form.save(commit=False)
            if not booking.preSave():
               error_messages = 'This court Already Booked at This session, find another one'
               form.add_error(None, error_messages)
            else:   
               messages.success(request, "Booking Process Started")
               send_mail(
                  "Confirmation Email",
                  "You have successfuly booked a court at weTenn tennis center\n Names: " + form.cleaned_data['name'],
                  settings.EMAIL_HOST_USER,
                  [form.cleaned_data['email']],
                  fail_silently=False,
               )
                  
               form = BookCourtForm()
         # return redirect()
      
   context = {'court': court, 'images': images, 'form': form}
   return render(request, "court.html", context)