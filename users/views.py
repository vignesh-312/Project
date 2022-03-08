from email import message
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Message, Profile, Skill
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles
from django.db.models import Q
# Create your views here.

def profiles(request):
    profiles = searchProfiles(request)
    page_profiles, paginator = paginateProfiles(request, profiles,3)
    context = {
        'profiles':profiles,
        'paginator': paginator,
    }
    return render(request, 'users/all-profiles.html',context)

def profile(request,pk):
    profile = Profile.objects.get(id=pk)
    
    topSkill = profile.skill_set.exclude(description = '')
    otherSkill = profile.skill_set.filter(description = '')
    
    context = {
        'profile':profile,
        'topSkill':topSkill,
        'otherSkill':otherSkill,
    }
    return render(request, 'users/single-profile.html',context)

def loginUser(request):
    
    page = 'login'
    if request.user.is_authenticated:
        return redirect('projects:projects')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
            # print('User does not exist')
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,'User logged in')
            return redirect(request.GET['next'] if 'next' in request.GET else 'users:account')
        else:
            messages.error(request,'Username or password does not match')
            #print('Username or password does not match')
    context = {}
    
    return render(request, 'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.success(request,'User logged out')
    return redirect('users:login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User created successfully')
            return redirect('users:login')
        else:
            messages.error(request,"Some error occured")
    context = {'page':page,'form':form}
    return render(request,'users/login_register.html',context)

@login_required(login_url='users:login')
def userAccount(request):
    profile = request.user.profile
    context = {'profile':profile}
    return render(request,'users/account.html', context)

@login_required(login_url='users:login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        form.save()
        messages.success(request,'Profile updated successfully')
        return redirect('users:account')
        
    context = {'form':form}
    return render(request,'users/edit-profile.html', context)


@login_required(login_url='users:login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill created successfully')
            return redirect('users:account')
        else:
            messages.error(request,'Some error occured')
    context = {'form':form,}
    return render(request,'users/skill-form.html',context)

@login_required(login_url='users:login')
def updateSkill(request,pk):
    profile = request.user.profile
    skillobj = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skillobj)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skillobj)
        if form.is_valid():
            form.save()
            messages.success(request,'Skill updated successfully')
            return redirect('users:account')
        else:
            messages.error(request,'Some error occured')
    context = {'form':form,}
    return render(request,'users/skill-form.html',context)

@login_required(login_url='users:login')
def deleteSkill(request,pk):
    profile = request.user.profile
    skillobj = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skillobj.delete()
        messages.success(request,'Skill deleted successfully')
        return redirect('users:account')
    
    context = {'object':skillobj,}
    return render(request,'delete.html',context)

@login_required(login_url='users:login')
def inbox(request):
    recipient = request.user.profile
    received_msgs = recipient.messages.all
    unreadCount = received_msgs.filter(is_read=False).count()
        
    context = {'received_msgs':received_msgs, 'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='users:login')
def viewMessage(request,pk):
    message = Message.objects.get(id=pk)

    if message.is_read == False:
        message.is_read == True
        message.save()
        
    context = {'message':message,}
    return render(request,'users/message.html',context)

def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        try:
            sender = request.user.profile
        except:
            sender = None
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save()
            return redirect('users:all-profile')

    context = {'form': form, 'recipient': recipient}
    return render(request, 'users/message-form.html',context)
    




