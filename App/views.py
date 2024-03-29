from django.shortcuts import render
from App.models import Court, Image
from .forms import BookCourtForm

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
   context = {'court': court, 'images': images, 'form': form}
   return render(request, "court.html", context)