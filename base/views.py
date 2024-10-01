from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponse
from django.db.models import Q
from .models import User, Room, Topic, Message
from .forms import RoomForm, UserForm, TopicForm, CustomUserCreationForm
# Create your views here.

def loginPage(request):
    page = 'login'
# Check If User Is Already Logged In
    if request.user.is_authenticated:
        return redirect('home')
# Get User Input
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
# Check That User Exists
        try:
            user = User.objects.get(email=email)
        except:
            context = {'error': 'email does not exist'}
# Check User Credentials
        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request, user)
            if request.GET.get('next') != None:
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')
        else:
            context = {'error': 'Wrong email or password'}
# Render Login Page
    context['page'] = page
    return render(request,'base/login_register.html', context)

def registerPage(request):
    page = 'register'
    form = CustomUserCreationForm()

# Check If User Is Already Logged In
    if request.user.is_authenticated:
        return redirect('home')
    
# Get User Input
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            return redirect('home')
# Render Register Page
    context = {'form': form, 'page': page}
    return render(request,'base/login_register.html', context)
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def updateUser(request):
    form = UserForm(instance=request.user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', id=request.user.id)
    return render(request,'base/update-user.html', {'form': form})

def home(request):
    q = request.POST.get('q') if request.POST.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q)|
        Q(name__icontains = q)|
        Q(description__icontains = q)
        ) if q != '' else Room.objects.all()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q)) if q != '' else Message.objects.all()
    room_count = rooms.count()
    topics = Topic.objects.all();
    context = {
            'rooms': rooms,
            'topics': topics,
            'room_count': room_count,
            'room_messages': room_messages
            }
    return render(request,'base/home.html', context)

def room(request, id):
    room = Room.objects.get(id=id)
    messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', id=room.id)
    
    context = {'room': room, 'messages': messages, 'participants': participants}
    return render(request,'base/room.html', context)

def userProfile(request, id):
    user = User.objects.get(id=id)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request,'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()

    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form': form, 'page': 'create'}
    return render(request,'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, id):
    room = Room.objects.get(id=id)
    form = RoomForm(instance=room)

    if room.host != request.user and request.user.is_staff == False:
        return HttpResponse('You are not allowed here')
    if request.method =='POST':
        form= RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form, 'page': 'update'}
    return render(request, 'base/room_form.html', context)
@login_required(login_url='login')
def deleteRoom(request, id):
    room = Room.objects.get(id=id)
    if room.host != request.user and request.user.is_staff == False:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, id):
    message = Message.objects.get(id=id)

    if message.user != request.user and not request.user.is_staff:
        return HttpResponse('You are not allowed here')
    if request.method == 'POST':
        message.delete()
        return redirect('room', id=message.room.id)
    
    return render(request, 'base/delete.html', {'obj': message})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

@login_required(login_url='login')
def createTopic(request):
    page = 'create'
    form = TopicForm()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('topics')
    context = {'form': form, 'page': page}
    return render(request, 'base/topic_form.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activities.html', {'messages': room_messages})