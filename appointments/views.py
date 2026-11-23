from datetime import datetime
from django import forms
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods
from .models import Appointment


class RequestForm(forms.ModelForm):
    consent = forms.BooleanField(label="I agree that Aswathy and Rahul may use these details to arrange my appointment.")
    class Meta:
        model = Appointment
        fields = ["name","phone","language","date","time"]
        widgets = {"date":forms.DateInput(attrs={"type":"date"}),"time":forms.Select(choices=[("", "Choose a time")] + [(f"{h:02}:00", f"{h:02}:00") for h in [*range(9,17),19,20,21]])}

    def clean(self):
        values = super().clean()
        day, start = values.get("date"), values.get("time")
        if day and start and datetime.combine(day,start) <= timezone.localtime().replace(tzinfo=None):
            self.add_error("date","Choose a future session.")
        return values


@never_cache
@require_http_methods(["GET","POST"])
def book(request):
    form = RequestForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("received")
    return render(request,"practice_home.html",{"form":form})
