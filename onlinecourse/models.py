
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


class Instructor(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username


class Learner(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.user.username


class Question(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  content = models.CharField(max_length=500)
  grade = models.IntegerField(default=1)

  def __str__(self):
    return self.content

  @property
  def question_text(self):
    return self.content

  def is_get_score(self, selected_ids):
    correct_ids = set(
      self.choice_set.filter(
        is_correct=True
      ).values_list('id', flat=True)
    )

    selected_question_ids = set(
      self.choice_set.filter(
        id__in=selected_ids
      ).values_list('id', flat=True)
    )

    return correct_ids == selected_question_ids


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  content = models.CharField(max_length=200)
  is_correct = models.BooleanField(default=False)

  def __str__(self):
    return self.content


class Enrollment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  date_enrolled = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user.username} - {self.course.name}"


class Submission(models.Model):

  # Existing fields retained for database compatibility
  user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )

  question = models.ForeignKey(
    Question,
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )

  choice = models.ForeignKey(
    Choice,
    on_delete=models.CASCADE,
    related_name='old_submissions',
    null=True,
    blank=True
  )

  submitted_at = models.DateTimeField(auto_now_add=True)

  # Required submission fields
  enrollment = models.ForeignKey(
    Enrollment,
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )

  choices = models.ManyToManyField(
    Choice,
    related_name='submissions'
  )

  def __str__(self):
    if self.enrollment:
      return f"Submission by {self.enrollment.user.username}"

    if self.user:
      return f"Submission by {self.user.username}"

    return f"Submission {self.id}"
