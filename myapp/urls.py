from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
	path('signup', views.signup, name='signup' ),
	path('', views.home, name='home' ),
	path('tasks', views.tasks, name='tasks'),
	path('sigout', views.sigout, name='sigout'),
	path('sigin', views.sigin, name='sigin'),
	path('tasks/create', views.create_task, name='create_task'),
	path('tasks/<int:task_id>', views.task_detail, name='task_detail'),
	path('tasks/<int:task_id>/delet_task', views.delet_task, name='delet_task'),

]