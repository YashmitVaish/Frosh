from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from django.urls import path

from django.utils.html import format_html
from django.urls import reverse
from .models import Team, Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_number', 'question_text', 'answer', 'points']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 4}),
            'answer': forms.TextInput(attrs={'class': 'vTextField'}),
        }

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'score', 'current_question_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'members')
    ordering = ('-score', '-created_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'points', 'text_preview')
    ordering = ('question_number',)
    search_fields = ('text', 'answer')
    list_editable = ('points',)
    list_per_page = 20
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Question Preview'
