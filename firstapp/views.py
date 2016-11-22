from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, Http404

from firstapp.models import Article, Comment, Ticket, UserProfile
from firstapp.forms import CommentForm, MyinfoForm

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    article_list = Article.objects.all()
    page_robot = Paginator(article_list, 6)
    page_num = request.GET.get('page')
    try:
        article_list = page_robot.page(page_num)
    except EmptyPage:
        article_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        article_list = page_robot.page(1)

    context = {}
    context["article_list"] = article_list

    return render(request, 'index.html', context)


def detail(request, id):
    try:
        article = Article.objects.get(id=id)

        if request.method == "GET":
            form = CommentForm

        context = {}
        context["article"] = article
        context['form'] = form

        article.views += 1
        article.save()
        return render(request, 'detail.html', context)
    except ObjectDoesNotExist:
        raise Http404


def comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            comment = form.cleaned_data["comment"]
            article = Article.objects.get(id=id)
            c = Comment(name=name, comment=comment, belong_to=article)
            c.save()
            return redirect(to="detail", id=id)
    return redirect(to="detail", id=id)


def index_login(request):
    if isinstance(request.user, User):
        return redirect('index')

    if request.method == "GET":
        form = AuthenticationForm
        if request.GET.get('next'):
            ne = request.GET.get('next')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
        return redirect(to="index")

    context = {}
    context['form'] = form
    context['next'] = ne

    return render(request, 'login.html', context)


def index_register(request):
    if isinstance(request.user, User):
        return redirect('index')

    if request.method == "GET":
        form = UserCreationForm

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.filter(username=form.cleaned_data['username'])[0]
            userprofile = UserProfile(belong_to=user)
            userprofile.save()
            return redirect(to='login')

    context = {}
    context['form'] = form

    return render(request, 'register.html', context)


@login_required
def vote(request, id):
    voter_id = request.user.id

    try:
        # 如果找不到登陆用户对此篇文章的操作，就报错
        user_ticket_for_this_article = Ticket.objects.get(voter_id=voter_id, article_id=id)
        user_ticket_for_this_article.choice = request.POST["vote"]
        user_ticket_for_this_article.save()
    except ObjectDoesNotExist:
        new_ticket = Ticket(voter_id=voter_id, article_id=id, choice=request.POST["vote"])
        new_ticket.save()

    article = Article.objects.get(id=id)
    article.likes = Ticket.objects.filter(article=id, choice='like').count()
    article.save()

    return redirect(to="detail", id=id)


@login_required
def myinfo(request):
    userprofile = UserProfile.objects.filter(belong_to=request.user)[0]
    if request.method == 'GET':
        if userprofile:
            form = MyinfoForm(
                initial={'full_name': userprofile.full_name,
                         'gender': userprofile.gender}
            )
    context = {}
    context['form'] = form
    return render(request, 'myinfo.html', context)


@login_required
def myinfoupdate(request):
    if request.method == 'POST':
        form = MyinfoForm(request.POST, request.FILES)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            gender = form.cleaned_data['gender']
            avatar = form.cleaned_data['avatar']
            password = form.cleaned_data['password']

            if UserProfile.objects.filter(belong_to=request.user):
                userprofile = UserProfile.objects.filter(belong_to=request.user)[0]
                userprofile.full_name = full_name
                userprofile.gender = gender
                if avatar:
                    userprofile.avatar = avatar
                userprofile.save()
            else:
                userprofile = UserProfile(full_name=full_name, gender=gender, avatar=avatar, belong_to=request.user)
                userprofile.save()

            if password:
                user = request.user
                user.set_password(password)
                user.save()

        return redirect(to="myinfo")


@login_required
def mycollection(request):
    ticket_list = Ticket.objects.filter(voter_id=request.user)
    page_robot = Paginator(ticket_list, 3)
    page_num = request.GET.get('page')
    try:
        ticket_list = page_robot.page(page_num)
    except EmptyPage:
        ticket_list = page_robot.page(page_robot.num_pages)
    except PageNotAnInteger:
        ticket_list = page_robot.page(1)

    context = {}
    context["ticket_list"] = ticket_list

    return render(request, 'mycollection.html', context)
