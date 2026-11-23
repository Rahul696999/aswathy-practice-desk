from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=16, validators=[RegexValidator(r"^\+?[0-9]{8,15}$", "Enter 8 to 15 digits, optionally starting with +.")])
    date = models.DateField()
    time = models.TimeField(help_text="One-hour sessions, India Standard Time.")
    language = models.CharField(max_length=12, choices=[(x,x) for x in ("Malayalam","English")])
    status = models.CharField(max_length=16, default="Pending", choices=[(x,x) for x in ("Pending","Confirmed","Rescheduled","Completed","Cancelled")])
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date","time"]
        constraints = [models.UniqueConstraint(fields=["date","time"], condition=models.Q(status__in=["Confirmed","Rescheduled"]), name="unique_reserved_slot")]

    def clean(self):
        if self.date and self.time:
            hours = range(9,17) if self.date.weekday() >= 5 else range(19,22)
            if self.time.hour not in hours or self.time.minute or self.time.second:
                raise ValidationError({"time":"Choose an available hourly start time."})

    def __str__(self):
        return f"{self.name} · {self.date} {self.time:%H:%M}"
