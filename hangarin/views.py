from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from .models import Task, Category, Priority
from .forms import TaskForm, CategoryForm, PriorityForm


# ==================== TASK VIEWS ==================== #

@login_required
def task_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')

    tasks = Task.objects.select_related('category', 'priority').all().order_by('-created_at')

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if status_filter:
        if status_filter.lower() == 'upcoming':
            tasks = tasks.filter(deadline__gt=timezone.now())
        else:
            tasks = tasks.filter(status__icontains=status_filter)

    if priority_filter:
        tasks = tasks.filter(priority__name__icontains=priority_filter)

    total_tasks_count = Task.objects.count()
    completed_count = Task.objects.filter(status__icontains='Completed').count()
    in_progress_count = Task.objects.filter(status__icontains='In Progress').count()
    pending_count = Task.objects.filter(status__icontains='Pending').count()
    upcoming_count = Task.objects.filter(deadline__gt=timezone.now()).count()
    high_priority_count = Task.objects.filter(priority__name__icontains='High').count()

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'hangarin/task_list.html', {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'total_tasks_count': total_tasks_count,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'pending_count': pending_count,
        'upcoming_count': upcoming_count,
        'high_priority_count': high_priority_count,
    })

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'hangarin/task_form.html', {'form': form, 'title': 'Add Task'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'hangarin/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'hangarin/task_confirm_delete.html', {'task': task})


# ==================== CATEGORY VIEWS ==================== #

@login_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'hangarin/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'hangarin/task_form.html', {'form': form, 'title': 'Add Category'})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'hangarin/task_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'hangarin/task_confirm_delete.html', {'task': category})


# ==================== PRIORITY VIEWS ==================== #

@login_required
def priority_list(request):
    priorities = Priority.objects.all().order_by('name')
    return render(request, 'hangarin/priority_list.html', {'priorities': priorities})

@login_required
def priority_create(request):
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm()
    return render(request, 'hangarin/task_form.html', {'form': form, 'title': 'Add Priority'})

@login_required
def priority_update(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        form = PriorityForm(request.POST, instance=priority)
        if form.is_valid():
            form.save()
            return redirect('priority_list')
    else:
        form = PriorityForm(instance=priority)
    return render(request, 'hangarin/task_form.html', {'form': form, 'title': 'Edit Priority'})

@login_required
def priority_delete(request, pk):
    priority = get_object_or_404(Priority, pk=pk)
    if request.method == 'POST':
        priority.delete()
        return redirect('priority_list')
    return render(request, 'hangarin/task_confirm_delete.html', {'task': priority})