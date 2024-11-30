from django.contrib import admin
from .models import Lesson, Timetable


class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'day_of_week', 'start_time', 'end_time', 'instructor', 'google_meet_link')
    search_fields = ('course__name', 'instructor__name', 'day_of_week')
    list_filter = ('day_of_week', 'course', 'instructor')

admin.site.register(Lesson, LessonAdmin)

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'subject', 'instructor', 'location', 'google_meet_link')
# Register your models here.
