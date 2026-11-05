
from django.shortcuts import render, get_object_or_404, redirect

from .models import (
  Course,
  Question,
  Choice,
  Submission,
  Enrollment
)


def course_details(request, course_id):
  course = get_object_or_404(Course, id=course_id)

  lessons = course.lesson_set.all()
  questions = course.question_set.all()

  return render(
    request,
    'onlinecourse/course_details_bootstrap.html',
    {
      'course': course,
      'lessons': lessons,
      'questions': questions
    }
  )


def submit(request, course_id):

  course = get_object_or_404(Course, id=course_id)

  if request.method == 'POST':

    if not request.user.is_authenticated:
      return redirect('admin:login')

    enrollment, created = Enrollment.objects.get_or_create(
      user=request.user,
      course=course
    )

    submission = Submission.objects.create(
      enrollment=enrollment
    )

    selected_ids = []

    for question in course.question_set.all():
      selected_ids.extend(
        request.POST.getlist(str(question.id))
      )

    selected_choices = Choice.objects.filter(
      question__course=course,
      id__in=selected_ids
    )

    submission.choices.set(selected_choices)

    return redirect(
      'show_exam_result',
      course_id=course.id,
      submission_id=submission.id
    )

  return redirect(
    'course_details',
    course_id=course_id
  )


def show_exam_result(request, course_id, submission_id):

  course = get_object_or_404(Course, id=course_id)

  submission = get_object_or_404(
    Submission,
    id=submission_id,
    enrollment__course=course
  )

  selected_choices = submission.choices.all()

  selected_ids = list(
    selected_choices.values_list('id', flat=True)
  )

  questions = course.question_set.all()

  grade = 0
  total = sum(question.grade for question in questions)

  question_results = []

  for question in questions:

    selected_question_choices = selected_choices.filter(
      question=question
    )

    correct_choices = question.choice_set.filter(
      is_correct=True
    )

    is_correct = question.is_get_score(selected_ids)

    if is_correct:
      grade += question.grade

    question_results.append({
      'question': question,
      'selected_choices': selected_question_choices,
      'correct_choices': correct_choices,
      'is_correct': is_correct
    })

  return render(
    request,
    'onlinecourse/exam_result.html',
    {
      'course': course,
      'submission': submission,
      'selected_ids': selected_ids,
      'grade': grade,
      'score': grade,
      'total': total,
      'question_results': question_results
    }
  )
