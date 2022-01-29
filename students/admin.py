from django.contrib import admin
from .models import Student, StudentGroup, Lesson, Discipline, Topic, TopicToLesson, TopicAssignment

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentGroup)
admin.site.register(Lesson)
admin.site.register(Discipline)
admin.site.register(Topic)
admin.site.register(TopicToLesson)
admin.site.register(TopicAssignment)