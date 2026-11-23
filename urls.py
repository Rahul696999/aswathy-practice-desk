from django.urls import path
from django.views.generic import TemplateView
from appointments.admin import desk
from appointments.views import book

urlpatterns = [path("",book,name="book"),path("received/",TemplateView.as_view(template_name="booking.html"),name="received"),path("staff/",desk.urls)]
