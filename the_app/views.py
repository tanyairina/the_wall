from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def success(request):
    if 'user' in request.session:
        user = User.objects.filter(id=request.session['id'])
        if user:
            context = {
                'user': user[0],
                'wall_messages': Wall_Message.objects.all()
            }
            return render(request, 'success.html', context)
    return redirect('/')

def register(request):
    print(request.POST)
    # Create a user object
    errors = User.objects.basic_validator(request.POST)
    print(errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.create(
        first_name=request.POST['fname'], 
        last_name=request.POST['lname'], 
        age=request.POST['age'],
        birth_date=request.POST['birth_date'],
        email=request.POST['email'], 
        password=request.POST['password'])
    request.session['user'] = user.first_name
    request.session['id'] = user.id
    return redirect('/success')

def login(request):
    print(request.POST)
    # retrieving a user from the db
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        user = user[0]
        if user.password == request.POST['password']:
            request.session['user'] = user.first_name
            request.session['id'] = user.id
            return redirect('/success')
    return redirect('/')

def logout(request):
    print(request.session)
    request.session.flush()
    print(request.session)
    return redirect('/')

def post_mess(request):
    Wall_Message.objects.create(
        message=request.POST['mess'],
        poster=User.objects.get(id=request.session['id'])
    )
    return redirect('/success')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(
        comment=request.POST['comment'], 
        poster=poster, 
        wall_message=message
    )
    return redirect('/success')

def profile(request, id):
    if 'user' in request.session:
        user = User.objects.filter(id=request.session['id'])
        if user:
            context = {
                'user': User.objects.get(id=id)
            }   
            return render(request, 'profile.html', context)
    return redirect('/')

def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/success')

def delete_comment(request, id):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect('/success')

def delete_post(request, id):
    wallpost = Wall_Message.objects.get(id=id)
    wallpost.delete()
    return redirect('/success')

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['fname']
    edit_user.last_name = request.POST['lname']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/success')