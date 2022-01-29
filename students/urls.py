from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('schedule/', views.schedule_view),
    path('', views.main_page),
    path('schedule/', views.schedule_view),
    path('lesson/<int:lesson_id>/', views.lesson_view),
    path('assign/<int:lessontopic_id>/', views.assign_topic_to_student),
    path('deassign/<int:assignment_id>/', views.deassign_topic_from_student),
    path('about/', views.about_view),
    
    path('user/', login_required(views.UserInfo.as_view())),
    path('lessons/', login_required(views.LessonInfo.as_view())),
    path('topics/<int:lesson_id>/', login_required(views.TopicByLessonInfo.as_view())),
    path('assign/<int:lessontopic_id>/', login_required(views.AssignTopic.as_view())),
    # path('', views.main_page)
]