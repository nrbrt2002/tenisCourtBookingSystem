from django.shortcuts import render, redirect
from App.models import Booking, Court, Image, Sessions
from .forms import BookCourtForm, AddImageForm
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import date

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

# Create your views here.

def home(request):
   courts = Court.objects.filter(is_available=True)
#    images = Image.objects.all();
   context = {'courts': courts}
   return render(request, 'home.html', context)

def login(request):
   return render(request, 'login.html')



@login_required
def dashboard(request):
   bookings = Booking.objects.filter(status = 'pendig').count()
   courts = Court.objects.count()
   sessions = Sessions.objects.count()
   images = Image.objects.count()
   contex = {'bookings': bookings, 'courts': courts, 'sessions': sessions, 'images': images}
   return render(request, 'dashboard.html', contex)

@login_required
def adminCourts(request):
   courts = Court.objects.all()
   context = {'courts': courts}
   return render(request, 'admin/admin-court.html', context)

@login_required
def changeAvailability(request, pk):
   
   if request.method == 'GET':
      state = request.GET.get('state')
      # try:
      court = Court.objects.get(id = pk)
      court.is_available = state
      court.save()
      messages.success(request, "Court details updated.")
      courts = Court.objects.all()
      context = {'courts': courts, 'messages': messages} 
      return redirect(request.META.get('HTTP_REFERER'))

@login_required
def dashboardSessions(request):
   sessions = Sessions.objects.all() 
   context = {'sessions': sessions}
   return render(request, 'admin/admin-sessions.html', context)

@login_required
def images(request):
   images = Image.objects.all()
   if request.method == 'POST':
      form = AddImageForm(request.POST, request.FILES)
      if form.is_valid():
         image = form.save(commit=False)
         now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
         
         # image.name = f"{now}_{form.cleaned_data['name']}"
         image.save()
         messages.success(request, "Image Added Successfuly")
   else:
      form = AddImageForm() 
   context = {'images': images, 'form': form}
   return render(request, 'admin/admin-images.html', context)

@login_required
def deleteImage(request, pk):
   if request.method == 'POST':
      image = Image.objects.get(id=pk)
      image.delete()
      messages.success(request, "Image Deleted Successfuly")
      return redirect('admin-images')

@login_required
def bookings(request):
   bookings = Booking.objects.all()
   context = {'bookings': bookings}
   return render(request, 'admin/admin-bookings.html', context)

@login_required
def refresh(request):
   
   booking = Booking.objects.filter(date__lt = date.today(), status ="pending").update(status = "cancled")
   messages.success(request, "Refresh complited")
   return redirect(dashboard)
   
   
def court(request, pk):
   initial_data = {
        'court_id': pk
    }
   form = BookCourtForm(initial=initial_data)
   court = Court.objects.get(id=pk)
   
   images = Image.objects.filter(court_id=pk)
   if request.method == 'POST':
      form = BookCourtForm(request.POST)
      if form.is_valid():
         with transaction.atomic():
            booking = form.save(commit=False)
            if booking.preSave() == False:
               error_messages = 'This court Already Booked at This session, find another one'
               form.add_error(None, error_messages)
               
            else:
               booking.save()
               booking_id = booking.id
               messages.success(request, "Booking Process Started")
               send_mail(
                  "Confirmation Email",
                  "You have successfully started booking a court at weTenn tennis center\n" +
                  "Names: " + form.cleaned_data['name'] + "\n" +
                  "Court Name: " + form.cleaned_data['court_id'].name + "\n" +
                  "Date: " + str(form.cleaned_data['date']) + "\n" +
                  "Session: " + form.cleaned_data['session_id'].name + "\n" +
                  f"Your booking Id is {booking_id}\n" +
                  "Now proceed with payment",
                  settings.EMAIL_HOST_USER,
                  [form.cleaned_data['email']],
                  fail_silently=False,
               )
               return redirect('checkout', pk=booking_id) 
      
   context = {'court': court, 'images': images, 'form': form}
   return render(request, "court.html", context)





def about(request):
   courts = Court.objects.count()
   sessions = Sessions.objects.count()
   contex = {"courts": courts, "sessions": sessions}
   return render (request, "about.html", contex)


def courts(request):
   courts = Court.objects.filter(is_available=True)
   context = {'courts': courts}
   return render(request, 'courts.html', context)

def support(request):
   success_message = ""
   if request.method == 'POST':
      email = request.POST.get('email')
      message = request.POST.get('message')
      send_mail(
                  "support Email",
                  message +"\n from --"+email,
                  settings.EMAIL_HOST_USER,
                  ['normuyomba@gmail.com'],
                  fail_silently=False,
               )
      success_message = "Your message has been submitted successfully! we'll contact you as soon"
   return render(request, 'support.html', {'success_message': success_message})

def sessions(request):
   sessions = Sessions.objects.filter()
   context = {'sessions': sessions}
   return render(request, 'sessions.html', context)





def checkout(request, pk):
   booking = Booking.objects.get(id = pk)
   host = request.get_host()
   paypal_checkout = {
      'business': settings.PAYPAL_RECEIVER_EMAIL,
      'amount': booking.session_id.price,
      'court_name': booking.court_id.name,
      'invoice': uuid.uuid4(),
      'currency_code': 'USD',
      'notify_url': f"http://{host}{reverse('paypal-ipn')}",
      'return_url': f"http://{host}{reverse('payment-successful', kwargs={'pk':booking.pk})}",
      'cancle_url': f"http://{host}{reverse('payment-failed', kwargs={'pk':booking.pk})}"
   }
   
   paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
   context = {'booking': booking, 'paypal': paypal_payment}
   
   return render(request, 'chekout.html',context)

def paymentSuccessful(request, pk):
   booking = Booking.objects.get(id=pk)
   if booking.status != 'paid':
      booking.status = 'paid'
      booking.save()
      send_mail(
                  "Payment Successful",
                  "You have complited you pament steps, see you at the court \n Thank you ",
                  settings.EMAIL_HOST_USER,
                  [booking.email],
                  fail_silently=False,
               )
   context = {'booking': booking}
   return render(request, 'payment-successful.html', context)

def paymentFailed(request, pk):
   booking = Booking.objects.get(id=pk)
   context = {'booking': booking}
   return render(request, 'payment-failed.html', context)