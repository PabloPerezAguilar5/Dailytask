from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Task
from user.models import User

# Create your views here.

@login_required
def task_list(request):
    # Obtener tareas del grupo familiar del usuario
    if request.user.family_group:
        family_tasks = Task.objects.filter(
            assigned_to__family_group=request.user.family_group
        ).order_by('-created_at')
    else:
        family_tasks = Task.objects.filter(assigned_to=request.user).order_by('-created_at')

    context = {
        'tasks': family_tasks,
        'family_members': User.objects.filter(family_group=request.user.family_group) if request.user.family_group else []
    }
    return render(request, 'tasks/task_list.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to_id = request.POST.get('assigned_to')
        points = request.POST.get('points', 10)
        priority = request.POST.get('priority', 'medium')
        due_date = request.POST.get('due_date')

        if not all([title, assigned_to_id]):
            return JsonResponse({'error': 'Título y usuario asignado son requeridos'}, status=400)

        try:
            assigned_to = User.objects.get(id=assigned_to_id)
            if request.user.family_group != assigned_to.family_group:
                return JsonResponse({'error': 'No puedes asignar tareas a usuarios de otro grupo familiar'}, status=400)

            task = Task.objects.create(
                title=title,
                description=description,
                created_by=request.user,
                assigned_to=assigned_to,
                points=points,
                priority=priority,
                due_date=due_date or timezone.now()
            )
            return JsonResponse({
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'points': task.points,
                    'status': task.status
                }
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Verificar que el usuario sea el asignado a la tarea
    if task.assigned_to != request.user:
        return JsonResponse({'error': 'No tienes permiso para completar esta tarea'}, status=403)
    
    if task.status == 'pending':
        task.complete()
        return JsonResponse({
            'success': True,
            'points': request.user.points,
            'task_id': task.id
        })
    
    return JsonResponse({'error': 'La tarea ya está completada'}, status=400)

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Verificar que el usuario pertenezca al mismo grupo familiar
    if (task.assigned_to.family_group != request.user.family_group and 
        task.created_by != request.user and 
        task.assigned_to != request.user):
        return JsonResponse({'error': 'No tienes permiso para ver esta tarea'}, status=403)
    
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def leaderboard(request):
    if request.user.family_group:
        members = User.objects.filter(
            family_group=request.user.family_group
        ).order_by('-points')
        
        leaderboard_data = [{
            'username': member.username,
            'points': member.points,
            'completed_tasks': member.assigned_tasks.filter(status='completed').count()
        } for member in members]
        
        return render(request, 'tasks/leaderboard.html', {
            'leaderboard': leaderboard_data
        })
    
    return redirect('profile')
