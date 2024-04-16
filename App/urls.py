from django.urls import path
from . import views
from django.urls import include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('dashboard/courts', views.adminCourts, name="admin-courts"), 
    path('dashboard/bookings', views.bookings, name="admin-bookings"),  
    path('dashboard/sessions', views.sessions, name="admin-sessions"), 
    path('dashboard/images', views.images, name="admin-images"), 
    path('dashboard/images/<str:pk>/', views.deleteImage, name="delete-image"), 
    path('dashboard/courts/<str:pk>/', views.changeAvailability, name="admin-courts-status"), 
    # path('accounts/logout', views.logout, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('court/<str:pk>/', views.court, name="court"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)