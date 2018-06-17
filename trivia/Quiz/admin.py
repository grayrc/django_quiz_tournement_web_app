from django.contrib import admin

from .models import Tournement, Question, Score

admin.site.register(Question)
admin.site.register(Score)

@admin.register(Tournement)
class TournementAdmin(admin.ModelAdmin):
    pass
