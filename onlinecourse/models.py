from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField()

  def __str__(self):
    return self.name


class Lesson(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  content = models.TextField()

  def __str__(self):
    return self.title


class Question(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  content = models.CharField(max_length=500)
  grade = models.IntegerField(default=1)

  def __str__(self):
    return self.content


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  content = models.CharField(max_length=200)
  is_correct = models.BooleanField(default=False)

  def __str__(self):
    return self.content


class Submission(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
  submitted_at = models.DateTimeField(auto_now_add=True)


class Enrollment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  date_enrolled = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user.username} - {self.course.name}"
