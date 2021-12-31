import os
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Knowledge, Person, Large, Middle, Task
from plotly.offline import plot
from plotly.tools import FigureFactory as ff
from django.db.models import Count
from .forms import CreateProjectForm, CreateLargeForm, CreateTaskForm, CreateMiddleForm, TaskEditForm, MiddleEditForm, LargeEditForm


def IndexView(request):
    """プロジェクトトップぺージ"""
    template = "dashboard.html"

    project = Project.objects.all()
    title = "Dashboard"
    project_form = CreateProjectForm
    """POST処理"""
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            new_project = form.save(commit=False)
            id = new_project.uuid
            new_project.save()

            return redirect('promane:project_detail', prj_id=id)

    context = {
        'project': project,
        'title': title,
        'project_form': project_form,
    }

    return render(request, template, context)


def ProjectView(request, prj_id):
    """プロジェクト詳細ぺージ"""
    template = "project_management.html"
    """"POST処理"""
    if request.method == "POST":
        if request.POST.get("form_type") == 'project':
            form = CreateProjectForm(request.POST)
            if form.is_valid():
                form.save()

                return redirect('promane:project_detail', prj_id=prj_id)

        elif request.POST.get("form_type") == 'large':
            form = CreateLargeForm(request.POST)
            if form.is_valid():
                new_large = form.save(commit=False)
                new_large.target_project = get_object_or_404(Project,
                                                             uuid=prj_id)
                new_large.save()

                return redirect('promane:project_detail', prj_id=prj_id)
    """前処理"""
    """チャート作成"""
    larges = Large.objects.filter(target_project__uuid=prj_id)
    df = []
    for ms in reversed(larges):
        df.append(
            dict(
                Task=ms.title,
                Start="{0:%Y-%m-%d %H:%M:%S}".format(ms.start),
                Finish="{0:%Y-%m-%d %H:%M:%S}".format(ms.finish),
            ))
    """大項目が無い場合エラーが発生する為、exceptで空のデータを渡す"""
    try:
        fig = ff.create_gantt(df,
                              title="日程",
                              bar_width=0.3,
                              showgrid_x=True,
                              showgrid_y=True,
                              height=500)
        plot_fig = plot(fig, output_type='div', include_plotlyjs=False)
    except:
        plot_fig = "<div style='height:500px;'>No chart</div>"
    """チャート作成終了"""
    """変数定義"""
    project = Project.objects.all()
    large = Large.objects.filter(target_project__uuid=prj_id)
    tasks_plan = Task.objects.filter(start__isnull=True).filter(
        target_middle__target_large__target_project__uuid=prj_id).order_by(
            'plan_to_start')
    tasks_ongoing = Task.objects.filter(start__isnull=False).filter(
        finish__isnull=True).filter(
            target_middle__target_large__target_project__uuid=prj_id).order_by(
                'plan_to_finish')
    tasks_done = Task.objects.filter(finish__isnull=False).filter(
        target_middle__target_large__target_project__uuid=prj_id).order_by(
            '-finish')
    project_form = CreateProjectForm
    large_form = CreateLargeForm
    title = get_object_or_404(Project, uuid=prj_id).name
    today = date.today()
    one_week_later = today + timedelta(days=7)
    target_project = get_object_or_404(Project, uuid=prj_id)
    target_project_id = target_project.uuid

    context = {
        'project': project,
        'large': large,
        'chart': plot_fig,
        'tasks_plan': tasks_plan,
        'tasks_ongoing': tasks_ongoing,
        'tasks_done': tasks_done,
        'project_form': project_form,
        'large_form': large_form,
        'title': title,
        'today': today,
        'one_week_later': one_week_later,
        'target_project_id': target_project_id,
    }

    return render(request, template, context)


def LargeEditView(request, prj_id, title):
    """大項目編集ページ"""
    template = "large_edit.html"
    """前処理"""
    large = get_object_or_404(Large, title=title)
    """"POST処理"""
    if request.method == "POST":
        form = LargeEditForm(request.POST, instance=large)
        if form.is_valid():
            form.save()

            return redirect('promane:project_detail', prj_id=prj_id)
    """変数定義"""
    project = Project.objects.all()
    large_edit_form = LargeEditForm(instance=large)
    target_project = get_object_or_404(Project, uuid=prj_id)
    target_project_id = target_project.uuid
    title = "Large Edit"

    context = {
        'project': project,
        'large_edit_form': large_edit_form,
        'target_project_id': target_project_id,
        'title': title,
    }

    return render(request, template, context)


def MiddleEditView(request, prj_id, title):
    """中項目編集ページ"""
    template = "middle_edit.html"
    """前処理"""
    middle = get_object_or_404(Middle, title=title)
    """"POST処理"""
    if request.method == "POST":
        form = MiddleEditForm(request.POST, instance=middle)
        if form.is_valid():
            form.save()

            return redirect('promane:project_detail', prj_id=prj_id)
    """変数定義"""
    project = Project.objects.all()
    middle_edit_form = MiddleEditForm(instance=middle)
    target_project = get_object_or_404(Project, uuid=prj_id)
    target_project_id = target_project.uuid
    title = "Middle Edit"

    context = {
        'project': project,
        'middle_edit_form': middle_edit_form,
        'target_project_id': target_project_id,
        'title': title,
    }

    return render(request, template, context)


def TaskEditView(request, prj_id, title):
    """実施項目編集ページ"""
    template = "task_edit.html"
    """前処理"""
    task = get_object_or_404(Task, title=title)
    """"POST処理"""
    if request.method == "POST":
        form = TaskEditForm(request.POST, instance=task)
        if form.is_valid():
            form.save()

            return redirect('promane:project_detail', prj_id=prj_id)
    """変数定義"""
    project = Project.objects.all()
    task_edit_form = TaskEditForm(instance=task)
    target_project = get_object_or_404(Project, uuid=prj_id)
    target_project_id = target_project.uuid
    title = "Task Edit"

    context = {
        'project': project,
        'task_edit_form': task_edit_form,
        'target_project_id': target_project_id,
        'title': title,
    }

    return render(request, template, context)


def TaskCreateView(request, prj_id, title):
    """実施項目追加ページ"""
    template = "add_task.html"
    """POST処理"""
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.target_middle = get_object_or_404(Middle, title=title)
            new_task.save()
            form.save_m2m()

            return redirect('promane:project_detail', prj_id=prj_id)
    """変数定義"""
    project = Project.objects.all()
    create_task_form = CreateTaskForm
    target_project = get_object_or_404(Project, uuid=prj_id)
    target_project_id = target_project.uuid
    title = "New Task"

    context = {
        'project': project,
        'create_task_form': create_task_form,
        'target_project_id': target_project_id,
        'title': title,
    }

    return render(request, template, context)


def MiddleCreateView(request, prj_id, title):
    """中項目追加ページ"""
    template = "add_middle.html"
    """"POST処理"""
    if request.method == "POST":
        form = CreateMiddleForm(request.POST)
        if form.is_valid():
            new_middle = form.save(commit=False)
            new_middle.target_large = get_object_or_404(Large, title=title)
            new_middle.save()

            return redirect('promane:project_detail', prj_id=prj_id)
    """変数定義"""
    project = Project.objects.all()
    create_middle_form = CreateMiddleForm
    target_project = get_object_or_404(Project, uuid=prj_id)
    target_project_id = target_project.uuid
    title = "New Middle"

    context = {
        'project': project,
        'create_middle_form': create_middle_form,
        'target_project_id': target_project_id,
        'title': title,
    }

    return render(request, template, context)


def TaskStartView(request, prj_id, task_id):
    task = get_object_or_404(Task, uuid=task_id)
    task.start = date.today()
    task.save()
    return redirect('promane:project_detail', prj_id=prj_id)


def TaskFinishView(request, prj_id, task_id):
    task = get_object_or_404(Task, uuid=task_id)
    task.finish = date.today()
    task.save()
    return redirect('promane:project_detail', prj_id=prj_id)


def TaskDeleteView(request, prj_id, task_id):
    task = get_object_or_404(Task, uuid=task_id)
    task.delete()
    return redirect('promane:project_detail', prj_id=prj_id)


def MiddleDeleteView(request, prj_id, middle_id):
    middle = get_object_or_404(Middle, uuid=middle_id)
    middle.delete()
    return redirect('promane:project_detail', prj_id=prj_id)


def LargeDeleteView(request, prj_id, large_id):
    large = get_object_or_404(Large, uuid=large_id)
    large.delete()
    return redirect('promane:project_detail', prj_id=prj_id)
