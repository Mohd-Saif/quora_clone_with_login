from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm



# def home(request):
#     data = None
#     if request.user.is_authenticated:
#         questions = Question.objects.all()
#     return render(request, 'app/home.html', {'questions': questions})
# @login_required
def home(request):
    questions=None
    if request.user.is_authenticated:
        questions = Question.objects.all().order_by('-created_at')
    return render(request, 'app/home.html', {'questions': questions})

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.created_by = request.user
            q.save()
            return redirect('/')
    else:
        form = QuestionForm()
    return render(request, 'app/ask.html', {'form': form})

@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.created_by = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'app/detail.html', {'question': question, 'form': form})

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.likes.add(request.user)
    return redirect('question_detail', pk=answer.question.id)