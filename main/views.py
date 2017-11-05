from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from main.models import *

from main.rec_sys.predict_nearest import *


def homepage(request):
    recs = []
    if request.user.is_authenticated():
        logged = True
        beers = list(Recommendation.objects.filter(user_id=request.user.id).values_list('beer', 'mark'))
        beers_id = [i[0] for i in beers]
        marks = [i[1] for i in beers]
        pred_recs = pred_by_dists(beers_id, marks)
        for i in range(len(pred_recs)):
            recs.append('<a href="' + pred_recs[i].replace(' ', '_').lower() + '">' + pred_recs[i] + '</a>')
        print(request.user.id)
    else:
        logged = False
    return render(request, 'homepage.html', {'recs': recs, 'logged': logged, 'username': request.user.username})


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        if len(name) < 1:
            return render(request, 'register.html', {'error': 'Слишком короткое имя'})
        if len(name) > 30:
            return render(request, 'register.html', {'error': 'Слишком большое имя'})
        if len(password) < 5:
            return render(request, 'register.html', {'error': 'Слишком короткий пароль'})
        if "@" not in email:
            return render(request, 'register.html', {'error': 'Некорректно введен email'})
        if User.objects.filter(username=name).exists() or \
                User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Пользователь с таким именем или почтой уже существует'})

        User.objects.create_user(name, email, password)

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)

        return redirect('/')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):

        name = request.POST['name']

        password = request.POST['password']
        try:
            name = User.objects.get(email=name).username
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Такой пользователь уже существует'})


def logout_view(request):
    logout(request)
    return redirect('/')


def beersearch(request):
    search_field = request.GET['search_field'].lower()
    beers = []
    answer = []
    for i in list(Beer.objects.all()):
        beers.append(i.name.lower())

    for i in beers:
        if search_field in i:
            answer.append('<a href="' + i.replace(' ', '_') + '">' + i.replace(search_field, "<strong>" + search_field + "</strong>") + '</a>')

    return render(request, 'search.html', {'answer': answer, 'search_field': search_field})


class make_url(View):
    def get(self, request, name):
        name = name.replace('_', ' ')
        beer = Beer.objects.get(name_lower=name)
        try:
            val = list(Recommendation.objects.filter(user_id=request.user.id, beer=beer.id).values_list('mark'))[0][0]
        except:
            val = None
        return render(request, 'pivo.html', {'beer': beer, 'val': val, 'username': request.user.username})


@login_required
@csrf_exempt
def apimark(request):
    beer_id = request.POST['beer_id']
    mark = request.POST['mark']
    beer_name = '/' + request.POST['beer_name'].replace(' ', '_').lower()
    Recommendation.objects.update_or_create(beer_id=beer_id, user=request.user, defaults={'mark': mark})

    beers = []

    return redirect(beer_name)
