from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task

def signup( request ):

	if request.method == 'GET':
		return render( request, 'myapp/signup.html', {
			'form': UserCreationForm
			})
	else:
		if request.POST['password1'] == request.POST['password2']:

			try:
				user = User.objects.create_user( 
					username=request.POST['username'],
					password=request.POST['password1'],
					)
				user.save()
				login( request, user)
				return redirect('myapp:tasks')
			except IntegrityError:
				return render( request, 'myapp/signup.html', {
					'form': UserCreationForm,
					'error': 'Usuario ya existente'
				})

		else:
			return render( request, 'myapp/signup.html', {
					'form': UserCreationForm,
					'error': 'Contrasenias no coincidentes'
				})

def home( request ):
	return render( request, 'myapp/home.html')

def tasks( request ):
	tasks = Task.objects.filter( user=request.user )
	return render( request, 'myapp/tasks.html', {
		'tasks': tasks
		})

def sigout( request ):
	logout( request )
	return redirect('myapp:home')

def sigin( request ):

	if request.method == 'GET':
		return render( request, 'myapp/sigin.html', {
			'form': AuthenticationForm
			})
	else:

		user = authenticate( request, 
			username=request.POST['username'], 
			password=request.POST['password'] )

		if user is None:
			return render( request, 'myapp/sigin.html', {
				'form': AuthenticationForm,
				'error': 'Usuario o contrasenia incorrectos'
				})
		else:
			login( request, user)
			return redirect('myapp:tasks')


def create_task( request ):

	if request.method == 'GET':
		return render( request, 'myapp/create_task.html', {
			'form': TaskForm
			})
	else:
		try:
			new_task = TaskForm(request.POST).save( commit=False)
			new_task.user = request.user
			new_task.save()
			return redirect('myapp:tasks')
		except ValueError:
			return render( request, 'myapp/create_task.html', {
				'form': TaskForm,
				'error': 'Ingrese un dato valido'
				})			

def task_detail( request, task_id ):

	task = get_object_or_404( Task, pk=task_id, user=request.user)

	if request.method == 'GET':
		update_task = TaskForm(instance=task)
		return render( request, 'myapp/task_detail.html', {'task':task, 'form':update_task})
	else:
		form = TaskForm(request.POST, instance=task)
		form.save()
		return redirect('myapp:tasks')

def delet_task( request, task_id):

	if request.method == 'GET':
		task = get_object_or_404( Task, pk=task_id, user=request.user)
		task.delete()
		return redirect('myapp:tasks')