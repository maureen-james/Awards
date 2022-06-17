from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse,Http404
from awards.forms import AddProjectForm, ProjectForm,DetailsForm,RatingForm
from awards.permissions import IsAdminOrReadOnly
from .models import Project,Profile,Rating 
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer

# Create your views here.
User = get_user_model()

def welcome(request):
    project=Project.objects.all()
    if request.method=='POST':
        current_user=request.user
        form=AddProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.user=current_user
            project.save()
            messages.success(request,('Project was posted successfully!'))
            return redirect('welcome')
    else:
            form=AddProjectForm()
    return render(request,'index.html',{'form':form,'projects':project})
@login_required(login_url='/accounts/login/')
def profile(request, user_id):

    current_user=get_object_or_404(User,id=user_id)
    # current_user = request.user
    projects = Project.objects.filter(user=current_user)
    profile = Profile.objects.filter(id = current_user.id).first()
    form=ProjectForm()
    return render(request, 'profile.html', {"projects": projects,'form':form, "profile": profile})
  

def edit_profile(request,user_id):
    current_user=get_object_or_404(User,id=user_id)
    current_user = request.user
    if request.method == 'POST':
        form = DetailsForm(request.POST, request.FILES)
        if form.is_valid():
                Profile.objects.filter(id=current_user.profile.id).update(bio=form.cleaned_data["bio"])
                profile = Profile.objects.filter(id=current_user.profile.id).first()

                profile.save()
        return redirect('profile')

    else:
        form = DetailsForm()
    
    return render(request, 'update_profile.html',{"form": form})


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
  form=AddProjectForm()
  if 'search' in request.GET and request.GET['search']:
    
    title_search = request.GET.get('search')
    print(title_search)
    searched_projects = Project.search_by_title(title_search)
  
    message = f"{title_search}"
    return render(request, 'search.html', {"message":message, "projects":searched_projects,"form":form})
  else:
    message = "You have not yet made a search"

    return render(request, 'search.html', {"message":message})

@login_required(login_url='/accounts/login/')
def add_project(request):
    if request.method == "POST":
        form = AddProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            form.instance.user = request.user
            project.save()
        return redirect('welcome')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {"form": form})

@login_required(login_url="/accounts/login/")
def delete_project(request):
    project = Project.objects.get(id=id)
    project.delete_project()
    return redirect("/profile", {"success": "Deleted Project Successfully"})        
 

@login_required(login_url="/accounts/login/")
def rate_project(request, id):
    if request.method == "POST":

        project = Project.objects.get(id=id)
        current_user = request.user

        design_rate=request.POST["design"]
        usability_rate=request.POST["usability"]
        content_rate=request.POST["content"]

        Rating.objects.create(
            project=project,
            user=current_user,
            design_rate=design_rate,
            usability_rate=usability_rate,
            content_rate=content_rate,
            avg_rate=round((float(design_rate)+float(usability_rate)+float(content_rate))/3,2),
        )

       
        avg_rating= (int(design_rate)+int(usability_rate)+int(content_rate))/3

      
        project.rate=avg_rating
        project.update_project()

        return render(request, "project.html", {"success": "Project Rated Successfully", "project": project, "rating": Rating.objects.filter(project=project)})
    else:
        project = Project.objects.get(id=id)
        return render(request, "project.html", {"danger": "Project Rating Failed", "project": project})

class ProjectList(APIView):
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        permission_classes = (IsAdminOrReadOnly,)
        return Response(serializers.data)
class ProfileList(APIView):
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        permission_classes = (IsAdminOrReadOnly,)
        return Response(serializers.data)          
   