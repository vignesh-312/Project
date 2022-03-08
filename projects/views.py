from multiprocessing import context
import profile
import re
from turtle import title
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Project,Review,Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchProjects, paginateProjects

def projects(request):
    projects=searchProjects(request)
    page_projects, custom_range = paginateProjects(request, projects, 3)
    context = {
        'projects':projects,
        'custom_range': custom_range,
    }
    return render(request,'projects/projects.html',context)

def project(request, pk):
    
    proj_obj = Project.objects.get(id=pk)
    
    tags = proj_obj.tags.all()

    reviews = proj_obj.review_set.all()
    
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = proj_obj
            review.owner = request.user.profile
            review.save()
            
            proj_obj.getVoteCount
            
            messages.success(request,'Your review was submitted successfully')
            return redirect('projects:project',pk=proj_obj.id)
        else:
            messages.error(request,'Some error Occurred')
    
    context = {
        'proj':proj_obj,'tags':tags, 'reviews':reviews, 'form': form
    }
    return render(request,'project/project.html',context)

@login_required(login_url='users:login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('users:account')
    context = {'form':form,}
    return render(request,'projects/project-form.html',context)

@login_required(login_url='users:login')
def updateProject(request,pk):
    profile = request.user.profile
    projectObj = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projectObj)
    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=projectObj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully')
            return redirect('users:account')
    context = {'form':form,}
    return render(request,'projects/project-form.html',context)

@login_required(login_url='users:login')
def deleteProject(request,pk):
    profile = request.user.profile
    projObj = profile.project_set.get(id=pk)
    if request.method == 'POST':
        projObj.delete()
        messages.success(request, 'Project deleted successfully')
        return redirect('users:account')
    context = {'object':projObj,}
    return render(request,'delete.html',context)

