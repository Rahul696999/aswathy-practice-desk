from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.utils import timezone
from .models import Appointment


class BookingTests(TestCase):
    def setUp(self):
        day = timezone.localdate()+timedelta(days=7)
        self.data = dict(name="Test Client",phone="9000000000",language="Malayalam",date=day,time="09:00" if day.weekday()>=5 else "19:00",consent="on")

    def test_intake(self):
        self.assertRedirects(self.client.post("/",self.data),"/received/")
        self.assertEqual(Appointment.objects.get().status,"Pending")

    def test_validation(self):
        self.client.post("/",dict(self.data,time="02:00"))
        self.client.post("/",dict(self.data,consent=""))
        self.assertFalse(Appointment.objects.exists())

    def test_staff_and_privacy(self):
        self.client.post("/",self.data)
        url="/staff/appointments/appointment/"
        self.assertEqual(self.client.get(url).status_code,302)
        for name in ["rahul","aswathy","another"]:
            user=get_user_model().objects.create(username=name,is_staff=True)
            user.user_permissions.add(Permission.objects.get(codename="view_appointment"))
            self.client.force_login(user)
            response=self.client.get(url)
            if name=="another":
                self.assertEqual(response.status_code,302)
            else:
                self.assertContains(response,"Test Client")
