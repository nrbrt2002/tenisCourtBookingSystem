from django import forms
from App.models import Booking, Image

class BookCourtForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['status']
        widgets={
            'date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'session_id': forms.Select(attrs={'class': 'form-select'}),
            'court_id': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        
class AddImageForm(forms.ModelForm):
    class Meta:
        model = Image
        field = '__all__'
        exclude = []
        widgets={
            # 'name':forms.FileInput(attrs={'class': 'form-control'}),
            'court_id':forms.Select(attrs={'class': 'form-control'}),
            'caption':forms.TextInput(attrs={'class': 'form-control'}),
        }

        