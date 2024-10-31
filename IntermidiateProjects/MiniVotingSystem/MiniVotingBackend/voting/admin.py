from django.contrib import admin

from voting.models import Candidate, CustomUser,Election, Vote

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Vote)
admin.site.register( Election)
admin.site.register(CustomUser)