from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentGroup(models.Model):
    group_id = models.OneToOneField(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_id.name

@receiver(post_save, sender=Group)
def create_student(sender, instance, created, **other):
    if created:
        StudentGroup.objects.create(group_id=instance)

class Student(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    sgroup_id = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True)
    bio = models.TextField(max_length=1000, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user_id.first_name} {self.user_id.last_name}"

@receiver(post_save, sender=User)
def create_student(sender, instance, created, **other):
    if created:
        Student.objects.create(user_id=instance)


class Discipline(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    group_id = models.ForeignKey(StudentGroup, on_delete=models.PROTECT)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.PROTECT)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.discipline_id.name} ({self.group_id.group_id.name}) {self.date} {self.start_time}-{self.end_time}"

    def to_json(self):
        return {
            'id' : self.pk,
            'discipline' : self.discipline_id.name,
            'group' : self.group_id.group_id.name,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
        }

class Topic(models.Model):
    title = models.CharField(max_length=100)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

class TopicToLesson(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.PROTECT)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.topic_id} {self.lesson_id}"

    def to_json(self):
        return {
            'id' : self.pk,
            'topic_id' : self.topic_id.pk,
            'topic_title' : self.topic_id.title
        }

class TopicAssignment(models.Model):
    lessontopic_id = models.ForeignKey(TopicToLesson, on_delete=models.PROTECT)
    student_id = models.ForeignKey(Student, on_delete=models.PROTECT)
    submitted = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.student_id} ({self.lessontopic_id})"

    def to_json(self):
        data = {
            'student_id' : self.student_id.pk,
            'lessontopic_id': self.lessontopic_id.pk,
        }
        if self.submitted != None:
            data += { 'submitted': self.submitted }
        return data