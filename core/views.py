from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Team, Question
from .forms import Registerteam, Answer, addques
from django.db import models

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_page')
        return redirect('question')
    return render(request,"home.html")

def rules(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_page')
        return redirect('question')
    return render(request, 'rules.html')

def register(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_page')
        return redirect('question')
    if request.method == "POST":
        form = Registerteam(request.POST)
        if form.is_valid():
            user = form.save_data()
            login(request,user)
            return redirect("question")
    else:
        form = Registerteam()
    return render(request, "register.html",{'form':form})


def post_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_page')
        return redirect('question')
    return redirect('home')

@login_required
def question(request):
    if request.user.is_superuser:
        return redirect('admin_page')
    team = request.user.team
    try:
        current_question = Question.objects.get(question_number=team.current_question_number)
    except Question.DoesNotExist:
        return render(request, 'question.html', {'completed': True})
    
    if request.method == 'POST':
        form = Answer(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer'].strip().lower()
            if answer == current_question.answer.lower():
                team.current_question_number += 1
                team.score += current_question.points
                team.save()
                messages.success(request, 'Correct! Moving to next question.')
                return redirect('question')
            else:
                messages.error(request, 'Wrong answer! Try again.')
    else:
        form = Answer()

    return render(request, 'question.html', {
        'question': current_question,
        'form': form,
        'team': team
    })

@user_passes_test(lambda u : u.is_superuser)
def admin_page(request):
    teams = Team.objects.all()
    query = request.GET.get('q','')
    if query:
        teams = teams.filter(
            models.Q(user__username__icontains=query) |
            models.Q(name__icontains=query) |
            models.Q(members__icontains=query)
        )
    return render(request,"admin_page.html", {'teams':teams,'query':query})
    

@login_required
def leaderboard(request):
    team = Team.objects.all()
    return render(request, "leaderboard.html",{'teams' : team})

def login_page(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_page')
        return redirect('question')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect('admin_page')
            return redirect('question')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

@user_passes_test(lambda u: u.is_superuser)
def question_list(request):
    questions = Question.objects.all().order_by('question_number')
    return render(request, 'question_list.html', {'questions': questions})

@user_passes_test(lambda u: u.is_superuser)
def add_question(request):
    if request.method == 'POST':
        form = addques(request.POST)
        if form.is_valid():
            Question.objects.create(
                question_number=form.cleaned_data['question_number'],
                points=form.cleaned_data['points'],
                question_text=form.cleaned_data['question_text'],
                answer=form.cleaned_data['answer']
            )
            messages.success(request, 'Question added successfully!')
            return redirect('question_list')
    else:
        form = addques()
    return render(request, 'question_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = addques(request.POST)
        if form.is_valid():
            question.question_number = form.cleaned_data['question_number']
            question.points = form.cleaned_data['points']
            question.question_text = form.cleaned_data['question_text']
            question.answer = form.cleaned_data['answer']
            question.save()
            messages.success(request, 'Question updated successfully!')
            return redirect('question_list')
    else:
        form = addques(initial={
            'question_number': question.question_number,
            'points': question.points,
            'question_text': question.question_text,
            'answer': question.answer
        })
    return render(request, 'question_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return redirect('question_list')
    return render(request, 'question_confirm_delete.html', {'question': question})


