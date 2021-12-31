from django import forms
from .models import Project, Large, Middle, Task
from django.core.exceptions import ValidationError


class CreateProjectForm(forms.ModelForm):
    """プロジェクト作成フォーム"""
    class Meta:
        model = Project
        exclude = ('uuid',)

class CreateLargeForm(forms.ModelForm):
    """大項目作成フォーム"""
    class Meta:
        model = Large
        exclude = ('target_project', 'uuid',)

class CreateMiddleForm(forms.ModelForm):
    """中項目作成フォーム"""
    class Meta:
        model = Middle
        exclude = ('target_large', 'uuid',)

class CreateTaskForm(forms.ModelForm):
    """実施項目作成フォーム"""
    class Meta:
        model = Task
        exclude = ('target_middle', 'uuid',)

class LargeEditForm(forms.ModelForm):
    """実施項目編集フォーム"""
    class Meta:
        model = Large
        exclude = ('target_project', 'uuid',)

class MiddleEditForm(forms.ModelForm):
    """実施項目編集フォーム"""
    class Meta:
        model = Middle
        exclude = ('target_large', 'uuid',)

class TaskEditForm(forms.ModelForm):
    """実施項目編集フォーム"""
    class Meta:
        model = Task
        exclude = ('target_middle', 'uuid',)
