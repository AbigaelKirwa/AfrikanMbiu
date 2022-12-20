from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.template import loader

from .models import Task

from django import forms
import os

# Create your views here.

class FileForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'media']

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args,**kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def  get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].count()


        DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

        img_folder_path = 'C:\Project\AfricanMbiu\media/videoandimage/22'
        dirListing = os.listdir(img_folder_path)
        newdirListing = len(dirListing) * 10

        context['count2'] = newdirListing

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__istartswith=search_input)

        context['search_input'] = search_input
        return (context)


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'media', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'media', 'complete']
    def index(request):
        if request.method == "POST":
            form = FileForm(request.POST, request.FILES)
            #form = Task(data = request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return HttpResponse("<h1> Uploaded successully </h1>")
        else:
            form = FileForm()
            #form - Task()
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name='task'
    success_url = reverse_lazy('tasks')











