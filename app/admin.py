from django.contrib import admin

from .models import *

# Register your models here
admin.site.register(Venue)
admin.site.register(Team)
admin.site.register(Mentor)
admin.site.register(Ticket)
admin.site.register(Judgement)