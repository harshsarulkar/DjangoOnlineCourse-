from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


class QuestionInline(admin.StackedInline):
  model = Question
  extra = 1


class ChoiceInline(admin.StackedInline):
  model = Choice
  extra = 2


class QuestionAdmin(admin.ModelAdmin):
  inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
  list_display = ('title', 'course')


class CourseAdmin(admin.ModelAdmin):
  inlines = [QuestionInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
