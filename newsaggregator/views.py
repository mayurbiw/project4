from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError
from newsaggregator.models import Categories, savedNews, UsersList
from django.contrib.auth.models import User
import json
from django.contrib.auth.hashers import check_password
from newsapi import NewsApiClient

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
          return render(request, "newsaggregator/login.html", {"message": None})

    newsapi = NewsApiClient(api_key='ead1421dd915459f8bd2b210b4972f83')

    request.session['cat'] = 'general'

    # /v2/top-headlines
    top_headlines = newsapi.get_top_headlines(language='en',
                                              country='us')
    ucat = []
    ul = UsersList.objects.filter(username = request.user.username)
    print(ul)
    for u in ul:
        uc  = u.categories.all()
        for i in uc:
            ucat.append(i.name)

    context = {
          "user": request.user,
          "articles" : top_headlines['articles'],
          "ucat":ucat,
          }
    print(top_headlines['articles'][0])
    return render(request, "newsaggregator/news.html",context)

def login_view(request):
    username =  request.POST.get('username', False)
    password =  request.POST.get('password', False)
    if username and password:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "newsaggregator/login.html", {"message": "Invalid credentials."})
    return render(request, "newsaggregator/login.html", {"message": ""})

def logout_view(request):
    logout(request)
    return render(request, "newsaggregator/login.html", {"message": "Logged out."})

def register_view(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    email = request.POST.get('email', False)
    first_name = request.POST.get('first_name', False)
    last_name = request.POST.get('last_name', False)
    if username and password and email and first_name and last_name:
        try:
            user = User.objects.create_user(username,email, password)
        except IntegrityError as e:
            return HttpResponse("User already exists " + str(e))
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return HttpResponseRedirect(reverse("selectCategories"))
    return render(request, "newsaggregator/register.html")

def profile_view(request):
    c = Categories.objects.all()
    sn = savedNews.objects.filter(username = request.user)
    context = {
    "categories":c,
    "user": request.user,
    "savedNews":sn,
    }
    return render(request, "newsaggregator/profile.html",context)

def selectCategories_view(request):
    c = Categories.objects.all()
    ucat = []
    ul = UsersList.objects.filter(username = request.user.username)
    print(ul)
    for u in ul:
        uc  = u.categories.all()
        for i in uc:
            ucat.append(i.name)
    print(c)
    print(ucat)
    context = {
    "categories":c,
    "ucat":ucat
    }
    return render(request, "newsaggregator/selectCategories.html",context)


def followCategory_view(request,category):
    ul = UsersList(username = request.user.username)
    c = Categories.objects.get(name = category)
    print(c)
    ul.save()
    ul.categories.add(c)
    data = {
    "success":True
    }
    print(json.dumps(data))
    return HttpResponse(json.dumps(data))


def unfollowCategory_view(request,category):
    c = Categories.objects.get(name = category)
    ul = UsersList.objects.get(username = request.user.username,categories=c)
    ul.delete()
    data = {
    "success":True
    }
    print(json.dumps(data))
    return HttpResponse(json.dumps(data))


def changePassword(request):
    oldpassword =  request.POST.get('oldpassword')
    newpassword =  request.POST.get('newpassword')
    currentpassword= request.user.password
    matchcheck= check_password(oldpassword, currentpassword)
    if matchcheck is True:
        request.user.set_password(newpassword)
        request.user.save()
        return HttpResponse("Your password has been changed")
    else:
        return HttpResponse("You entered the incorrect current password")

def fetchNews(request):
        category =  request.GET.get('button')
        newsapi = NewsApiClient(api_key='ead1421dd915459f8bd2b210b4972f83')
        request.session['cat'] = category
        # /v2/top-headlines
        top_headlines = newsapi.get_top_headlines(category=category,
                                                  language='en',
                                                  country='us')

        ucat = []
        ul = UsersList.objects.filter(username = request.user.username)
        print(ul)
        for u in ul:
            uc  = u.categories.all()
            for i in uc:
                ucat.append(i.name)
        context = {
              "user": request.user,
              "articles" : top_headlines['articles'],
              "ucat":ucat,
          }
        return render(request, "newsaggregator/news.html",context)

def readLater(request):
    link = request.GET.get('link')
    title = request.GET.get('title')
    cat = request.session['cat']
    sn = savedNews(username = request.user.username,link = link, title=title,category=cat)
    sn.save()
    data = {
    "success":True
    }
    return HttpResponse(json.dumps(data))

def fetchSearchedNews(request):
    q = request.GET.get('query')
    request.session['cat'] = q
    newsapi = NewsApiClient(api_key='ead1421dd915459f8bd2b210b4972f83')
    all_articles = newsapi.get_everything(q=q,
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

    ucat = []
    ul = UsersList.objects.filter(username = request.user.username)
    print(ul)
    for u in ul:
        uc  = u.categories.all()
        for i in uc:
            ucat.append(i.name)
    context = {
          "user": request.user,
          "articles" : all_articles['articles'],
          "ucat":ucat,

      }
    return render(request, "newsaggregator/news.html",context)
