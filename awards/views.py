from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse,Http404
from awards.forms import ProjectForm,UpdateProfileForm,RatingForm
from .models import Project,Profile,Rating 
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def home(request):
    project=Project.objects.all()
    if request.method=='POST':
        current_user=request.user
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.user=current_user
            project.save()
            messages.success(request,('Project was posted successfully!'))
            return redirect('home')
    else:
            form=ProjectForm()
    return render(request,'index.html',{'form':form,'projects':project})
@login_required(login_url='/accounts/login/')
def profile(request,user_id):

    current_user=get_object_or_404(User,id=user_id)
    # current_user = request.user
    projects = Project.objects.filter(user=current_user)
    profile = Profile.objects.filter(id = current_user.id).first()
    form=ProjectForm()
    return render(request, 'profile.html', {"projects": projects,'form':form, "profile": profile})
  
def update_profile(request):
  	#Get the profile
    current_user=request.user
    profile = Profile.objects.filter(id=current_user.id).first()
    if request.method == 'POST':
        profileform = UpdateProfileForm(request.POST,request.FILES,instance=profile)
        if  profileform.is_valid:
            profileform.save(commit=False)
            profileform.user=request.user
            profileform.save()
            return redirect('profile')
    else:
        form=UpdateProfileForm()
    return render(request,'update_profile.html',{'form':form})

@login_required(login_url='/accounts/login/')
def project_details(request, project_id):
  
  form = RatingForm(request.POST)
  try:
    project_details = Project.objects.get(pk = project_id)
    project_rates = Rating.objects.filter(project__id=project_id).all()
  except Project.DoesNotExist:
    raise Http404
  
  return render(request, 'project_details.html', {"details":project_details, "rates":project_rates, "form":form})
@login_required(login_url='/accounts/login/')
def search_results(request):
  form=ProjectForm()
  if 'search' in request.GET and request.GET['search']:
    
    title_search = request.GET.get('search')
    print(title_search)
    searched_projects = Project.search_by_title(title_search)
  
    message = f"{title_search}"
    return render(request, 'search.html', {"message":message, "projects":searched_projects,"form":form})
  else:
    message = "You have not yet made a search"

    return render(request, 'search.html', {"message":message})
   