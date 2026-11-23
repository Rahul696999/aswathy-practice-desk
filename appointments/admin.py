from django.contrib import admin
from .models import Appointment


class PracticeAdmin(admin.AdminSite):
    site_header = "Aswathy Venu · Practice desk"
    site_title = "Practice desk"
    index_title = "Appointment management"

    def has_permission(self, request):
        return super().has_permission(request) and request.user.username in {"aswathy","rahul"}


desk = PracticeAdmin(name="practice")

@admin.register(Appointment, site=desk)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["name","date","time","language","status"]
    search_fields = ["name","phone"]
    list_filter = ["status","language","date"]
    date_hierarchy = "date"
    readonly_fields = ["created"]
    list_per_page = 30
