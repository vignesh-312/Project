from .models import Skill,Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query)|
        Q(skill__in=skills)).distinct()
    
    return profiles

def paginateProfiles(request,profiles,no_of_prof):
    paginator = Paginator(profiles, no_of_prof)
    page = request.GET.get('page')
    try:
        page_profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_profiles = paginator.page(page)
    return page_profiles, paginator