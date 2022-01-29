from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views import View
from django.http import HttpResponse
from django.core.serializers import serialize

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student, Lesson, TopicToLesson, TopicAssignment

import datetime


def check_if_lesson_passed(lesson):
    return lesson.date < datetime.date.today() or lesson.date == datetime.date.today() and lesson.start_time < datetime.datetime.now().time()


def main_page(request):
    return render(request, 'main.html')

class UserInfo(View):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        student = Student.objects.get(user_id__exact=request.user.id)
        student_group = student.sgroup_id.group_id.name

        data = {
            'first_name': user.first_name,
            'last_name':user.last_name,
            'group_name': student_group
        }
        return HttpResponse(str(data))

class LessonInfo(View):
    def get(self, request, format=None):
        student = Student.objects.get(user_id__exact=request.user.id)
        student_group = student.sgroup_id

        lessons = [item.to_json() for item in Lesson.objects.filter(group_id__id__exact=student.sgroup_id.id).all()]
        return HttpResponse(str({'lessons' : lessons}))

class TopicByLessonInfo(View):
    def get(self, request, lesson_id,format=None):
        
        return HttpResponse(str(data))

class AssignTopic(View):
    # def get(self, request, lessontopic_id, format=None):
    #     # student = Student.objects.get(user_id__exact=request.user.id)
    #     lesson_id = TopicToLesson.objects.get(pk__exact=lessontopic_id).lesson_id.pk
    #     student_id = Student.objects.get(user_id__exact=request.user.id).pk

    #     student_assignments = TopicAssignment.objects.filter(student_id__user_id__pk__exact=request.user.id)
    #     assigned_topics = student_assignments.filter(lessontopic_id__lesson_id__pk__exact=lesson_id)
    #     if assigned_topics.count() > 0:
    #         response = HttpResponse("{ 'error': 'Student already has topic for this lesson' }")
    #         response.status_code = 409
    #         return response

    #     TopicAssignment.objects.create(lessontopic_id=lessontopic_id, student_id=student_id)
    #     return HttpResponse("{ 'status': 'OK' }")

    def post(self, request, lessontopic_id, format=None):
        
        if assigned_topics.count() > 0:
            response = HttpResponse("{ 'error': 'Student already has topic for this lesson' }")
            response.status_code = 409
            return response

        TopicAssignment.objects.create(lessontopic_id=lessontopic_id, student_id=student_id)
        return HttpResponse("{ 'status': 'OK' }")

@login_required
def user(request):
    user = request.user
    
    return { 'first_name': user.first_name, 'last_name': user.last_name, 'group_name': student_group }

@login_required
def schedule_view(request):
    fullname = f'{request.user.first_name} {request.user.last_name}'
    student = Student.objects.get(user_id__exact=request.user.id)
    student_group = student.sgroup_id.group_id.name
    print(student.sgroup_id.id)
    # print(Lesson.objects.raw(f'select * from students_lesson where group_id_id={student.sgroup_id.id}')[0])
    lessons = Lesson.objects.filter(group_id__id__exact=student.sgroup_id.id)
    previous_lessons, next_lessons = [], []
    for lesson in lessons:
        if check_if_lesson_passed(lesson):
            previous_lessons.append(lesson)
        else:
            next_lessons.append(lesson)
    
    # previous_lessons = lessons.filter(date__lt=datetime.date.today())
    # next_lessons = lessons.filter(date__gte=datetime.date.today())

    # print(Lesson.objects.all()[0].group_id.group_id.id)

    data = {
        'fullname': fullname, 
        'student_group': student_group, 
        'previous_lessons': previous_lessons,
        'next_lessons': next_lessons
    }

    return render(request, 'schedule.html', data)
    
@login_required
def lesson_view(request, lesson_id):
    student = Student.objects.get(user_id__exact=request.user.id)
    assigned_topics = TopicAssignment.objects.filter(lessontopic_id__lesson_id__pk__exact=lesson_id).filter(student_id__pk__exact=student.pk)
    print(assigned_topics)

    lesson = Lesson.objects.get(pk__exact=lesson_id)
    data = { 'lesson': lesson }
    lesson_passed = check_if_lesson_passed(lesson)
    data.update({ 'lesson_passed': lesson_passed })

    if assigned_topics.count() > 0:
        assigned_topic = assigned_topics[0]
        if lesson_passed and assigned_topic.submitted != None:
            data.update({ 'marked': True, 'credit': 'есть' if assigned_topic.submitted else 'нет' })
        data.update({ 'topic_assigned': True, 'assigned_topic': assigned_topic })
    else:
        lessontopics = TopicToLesson.objects.filter(lesson_id__exact=lesson_id)
        data.update({ 'topic_assigned': False, 'topics': lessontopics })

    return render(request, 'lesson.html', data)

@login_required
def assign_topic_to_student(request, lessontopic_id):
    lessontopic = TopicToLesson.objects.get(pk__exact=lessontopic_id)
    student = Student.objects.get(user_id__exact=request.user.id)

    TopicAssignment.objects.create(lessontopic_id=lessontopic, student_id=student, submitted=None)
    return HttpResponse('success')

@login_required
def deassign_topic_from_student(request, assignment_id):
    print('assignment_id:', assignment_id)
    TopicAssignment.objects.get(pk__exact=assignment_id).delete()
    return HttpResponse('success')

def about_view(request):
    return render(request, 'about.html')