from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Choice, Submission


def course_details(request, course_id):
  course = get_object_or_404(Course, id=course_id)
  lessons = course.lesson_set.all()
  questions = course.question_set.all()

  return render(request,
                'onlinecourse/course_details_bootstrap.html',
                {'course': course, 'lessons': lessons,
                 'questions': questions})


def submit(request, course_id):
  if request.method == 'POST':
    course = get_object_or_404(Course, id=course_id)
    questions = course.question_set.all()

    score = 0
    total = questions.count()

    for question in questions:
      selected_id = request.POST.get(str(question.id))

      if selected_id:
        choice = get_object_or_404(
          Choice, id=selected_id, question=question
        )

        Submission.objects.create(
          user=request.user,
          question=question,
          choice=choice
        )

        if choice.is_correct:
          score += question.grade

    request.session['score'] = score
    request.session['total'] = sum(q.grade for q in questions)

    return redirect('show_exam_result')

  return redirect('course_details', course_id=course_id)


def show_exam_result(request):
  score = request.session.get('score', 0)
  total = request.session.get('total', 0)

  return render(request, 'onlinecourse/exam_result.html', {
    'score': score,
    'total': total
  })
