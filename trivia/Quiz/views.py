from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Tournement
from .models import Question
from .models import Score
import requests
from datetime import datetime
import json
from random import shuffle


### functions for index
def addUser(request):

    user = User.objects.create_user(request.POST['user-name'], 'null', request.POST['password'])
    user.save()

## functions for tournements_home
def enterScore(user, t_id, score):
    print("enterScore t_id: " + str(t_id))
    t = Tournement.objects.get(id=t_id)

    s = Score(
        player_id = user,
        tournement_id = t,
        score = score
        )
    
    s.save()

## functions for create_tournement
def addTournement(request):
    entry = Tournement(
        name=request.POST['name'],
        difficulty=request.POST['difficulty'],
        category=request.POST['category'],
        start_time=request.POST['start-date'],
        end_time=request.POST['end-date']
    )
    entry.save()
    saveQuestions(entry)

def saveQuestions(entry):
    catId = getCategoryId(entry.category)
    d = 'medium'
    if entry.difficulty == 'e':
        d = 'easy'
    elif entry.difficulty == 'm':
        d = "medium"
    else:
        d = 'hard'
    url = "https://opentdb.com/api.php?amount=10&category=" + \
    str(catId) + "&difficulty=" + d + "&type=multiple"
    r = requests.get(url)
    data = r.json()
    questions = data['results']
    for q in questions:
        questionEntry = Question(
            tournement_id = entry,
            question_text = q['question'],
            correct_answer = q['correct_answer'],
            incorrect_one = q['incorrect_answers'][0],
            incorrect_two = q['incorrect_answers'][1],
            incorrect_three = q['incorrect_answers'][2]
        )
        questionEntry.save()

def getCatagories():
    catagories = getCategoryJson()
    category_names=[]
    for name in catagories:
        category_names.append(name['name'])
    return category_names

def getCategoryJson():
    url = 'https://opentdb.com/api_category.php'
    r = requests.get(url)
    data = r.json()
    return data['trivia_categories']

def getCategoryId(category):
    categories = getCategoryJson()
    id = -1
    for c in categories:
        if c['name'] == category:
            id = c['id']
    return id


## functions for tournement
def joinTournement(request):
    t_id = request.POST.get('tournement_to_join', False)
    t = Tournement.objects.get(pk=t_id)
    p = request.user
    t.players.add(p)

def getTournementContext(request, id):
    t = Tournement.objects.get(pk=id)
    players = [p.username for p in t.players.all()]

    notPlayed = True

    scores = Score.objects.filter(tournement_id=t)

    for s in scores:
        print(s.score)
        if s.player_id == request.user:
            notPlayed = False
    
    qs = t.players.all()
    played = list(qs)
    context = {
        'tournement': t,
        'players': players,
        'notPlayed': notPlayed,
    }
    return context

##function for view_current
def getCurrent():
    now = datetime.now()
    return Tournement.objects.filter(start_time__lte=now, end_time__gte=now)

## function for view_future
def getFuture():
    now = datetime.now()
    return Tournement.objects.filter(start_time__gte=now)

## functions for game
def setUpQuestions(request, id):
    qs = Question.objects.filter(tournement_id = id) 
    all_qs = []
    for q in qs:
        q_data = [q.id, q.question_text, q.correct_answer]
        answers = [
        q.correct_answer,
        q.incorrect_one,
        q.incorrect_two,
        q.incorrect_three
        ]
        shuffle(answers)
        q_data.append(answers)
        all_qs.append(q_data)
    
    request.session['all_qs'] = all_qs
    request.session['q_n'] = 0
    request.session['n_correct'] = 0
    return all_qs


## views
def index(request):
    if request.method == 'POST':
        addUser(request)
    return render(request, 'index.html')

@login_required
def tournements_home(request):
    if request.method == 'POST':
        t_id = request.POST['t_id']
        print(t_id)
        enterScore(request.user, t_id, request.session['n_correct'])
    
    return render(request, 'tournements_home.html')

@staff_member_required
def create_tournement(request):
    if request.method == 'POST':
        messages.success(request, "New Tournement Added")
        addTournement(request)

    template = loader.get_template('create_tournement.html')
    context = {
        'categories': getCatagories,
    }
    return HttpResponse(template.render(context, request))

def tournement(request, id):
    try:
        tournement = Tournement.objects.get(id=id)
    except Tournement.DoesNotExist:
        raise Http404('tournement not found')

    if request.method == 'POST':
        joinTournement(request)
    
    players = Tournement.objects.get(pk=id).players.all()
    players_list = [p.username for p in players]
    template = loader.get_template('tournement.html')
    context = getTournementContext(request, id)
    return HttpResponse(template.render(context, request))

def add_user(request):
    return render(request, 'add_user.html')

def view_current(request):
    template = loader.get_template('view_current.html')
    context = {
        'tournements': getCurrent,
    }
    return HttpResponse(template.render(context, request))

def view_future(request):
    template = loader.get_template('view_future.html')
    context = {
        'tournements': getFuture,
    }
    return HttpResponse(template.render(context, request))

@login_required
def game(request, id):
    try:
        game = Tournement.objects.get(id=id)
    except Tournement.DoesNotExist:
        raise Http404('tournement not found')

    feedback_string = "Let's get started!"
    feedback = ''
    if request.method != 'POST':
        all_qs = setUpQuestions(request, id)
        
    else:
        print(request.POST['correct'])
        print(request.POST.get('radio_answers', None))
        all_qs = request.session['all_qs']
        request.session['q_n'] = request.session['q_n'] + 1
        if request.POST.get('radio_answers', None) == request.POST['correct']:
            feedback_string = "Right Answer!!!"
            request.session['n_correct'] += 1
        else:
            feedback_string = "Wrong. The answer is: " + request.POST['correct']

    game_length = len(all_qs)
    
    if request.session['q_n'] >= game_length:
        current_question = ['','','',['','','','']]
        feedback_string += " End of quiz.You got " + str(request.session['n_correct']) + " out of 10 correct."
    else:
        current_question = all_qs[request.session['q_n']]

    answers = current_question[3]

    question = current_question[1].replace("&quot;", '"')
    question = question.replace("&#039;", "'")

    template = loader.get_template('game.html')
    context = {
        'feedback': feedback_string,
        'question': question,
        'answers': answers,
        'correct': current_question[2],
        'q_n': request.session['q_n'],
        'tournement_id': id
    }
    return HttpResponse(template.render(context, request))

def high_scores(request):
    
    template = loader.get_template('high_scores.html')
    context = {
        'highScores':Score.objects.order_by('-score')[:10]
    }
    return HttpResponse(template.render(context, request))
