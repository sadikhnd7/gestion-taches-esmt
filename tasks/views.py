from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile, Project
from django.utils import timezone
from django.db.models import Count, Q
from django.db.models import F
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(username=username, email=email, password=password)

        Profile.objects.create(user=user, role=role)

        login(request, user)

        return redirect('dashboard')


    return render(request, 'tasks/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'tasks/login.html', {'error': 'Identifiants incorrects'})
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    projects = (Project.objects.filter(members=request.user) | Project.objects.filter(created_by=request.user)).distinct()
    tasks = Task.objects.filter(assigned_to=request.user)

    return render(request, 'tasks/dashboard.html', {
        'projects': projects,
        'tasks': tasks
    })


from django.contrib.auth.decorators import login_required
from .models import Profile, Project, Task


@login_required
def create_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']


        Project.objects.create(name=name, description=description, created_by=request.user)

        return redirect('dashboard')

    return render(request, 'tasks/create_project.html')


@login_required
def edit_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project.name = request.POST['name']
        project.description = request.POST['description']
        project.save()
        return redirect('dashboard')

    return render(request, 'tasks/edit_project.html', {'project': project})

@login_required
def delete_project(request, pk):

        project = Project.objects.get(pk=pk)
        project.delete()
        return redirect('dashboard')

def project_detail(request, pk):
    pass

def task_detail(request, pk):
    pass
@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        status = request.POST['status']
        project = Project.objects.get(pk=request.POST['project'])
        assigned_to = User.objects.get(pk=request.POST['assigned_to'])
        created_by = request.user

        if project.created_by != request.user:
            return render(request, 'tasks/create_task.html', {'error': "Vous n'êtes pas le créateur de ce projet"})
        if request.user.profile.role == 'etudiant':
            if assigned_to.profile.role == 'professeur':
                return render(request, 'tasks/create_task.html',
                              {'error': "Un étudiant ne peut pas assigner un professeur"})


        Task.objects.create(title=title, description=description, deadline=deadline,status=status, project=project, assigned_to=assigned_to, created_by=request.user)

        return redirect('dashboard')
    projects = Project.objects.filter(created_by=request.user)
    users = User.objects.filter(profile__isnull=False)
    return render(request, 'tasks/create_task.html', {'projects':projects,'users': users})


@login_required
def edit_task(request, pk):
    task = Task.objects.get(pk=pk)

    if request.user != task.project.created_by and request.user != task.assigned_to:
        return redirect('dashboard')

    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.deadline = request.POST['deadline']
        task.status = request.POST['status']
        task.project = Project.objects.get(pk=request.POST['project'])
        assigned_to = User.objects.get(pk=request.POST['assigned_to'])

        if request.user.profile.role == 'etudiant':
            if assigned_to.profile.role == 'professeur':
                return render(request, 'tasks/edit_task.html', {
                    'task': task,
                    'projects': Project.objects.all(),
                    'users': User.objects.filter(profile__isnull=False),
                    'error': "Un étudiant ne peut pas assigner un professeur"
                })

        task.assigned_to = assigned_to
        task.save()
        return redirect('dashboard')

    return render(request, 'tasks/edit_task.html', {
        'task': task,
        'projects': Project.objects.all(),
        'users': User.objects.filter(profile__isnull=False)
    })

@login_required
def delete_task(request, pk):
    task = Task.objects.get(pk=pk)

    if request.user != task.project.created_by:
        return redirect('dashboard')

    task.delete()
    return redirect('dashboard')


@login_required
def stats(request):
    professeurs = User.objects.filter(profile__role='professeur')

    stats_data = []

    for prof in professeurs:
        total_tasks = Task.objects.filter(assigned_to=prof).count()

        tasks_in_time = Task.objects.filter(
            assigned_to=prof,
            status='done',
            completed_at__lte=F('deadline')
        ).count()

        if total_tasks > 0:
            percentage = (tasks_in_time / total_tasks) * 100
        else:
            percentage = 0

        if percentage == 100:
            prime = 100000
        elif percentage >= 90:
            prime = 30000
        else:
            prime = 0

        stats_data.append({
            'professeur': prof,
            'total_tasks': total_tasks,
            'tasks_in_time': tasks_in_time,
            'percentage': round(percentage, 2),
            'prime': prime
        })

    return render(request, 'tasks/stats.html', {'stats_data': stats_data})

@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        new_password = request.POST['password']

        request.user.username = username
        request.user.email = email

        if new_password:
            request.user.set_password(new_password)
            update_session_auth_hash(request, request.user)

        request.user.save()

        if request.FILES.get('avatar'):
            request.user.profile.avatar = request.FILES['avatar']
            request.user.profile.save()

        return redirect('dashboard')
    return render(request, 'tasks/profile.html')


@login_required
def add_member(request, pk):
    project = Project.objects.get(pk=pk)

    if project.created_by != request.user:
        return redirect('dashboard')

    if request.method == 'POST':
        user = User.objects.get(pk=request.POST['user'])
        project.members.add(user)
        return redirect('dashboard')

    users = User.objects.filter(profile__isnull=False)
    return render(request, 'tasks/add_member.html', {'project': project, 'users': users})