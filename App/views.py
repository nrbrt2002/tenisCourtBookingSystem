from django.shortcuts import render, redirect
from App.models import Booking, Court, Image
from .forms import BookCourtForm
from django.contrib import messages
from django.db import transaction
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
            if not booking.save():
               error_message = booking.error_message
               form.add_error(None, error_message)
         # form.save()
            else:
               form = BookCourtForm()
               messages.success(request, "Booking Process Started")
         
         # return redirect()
      
   context = {'court': court, 'images': images, 'form': form}
   return render(request, "court.html", context)