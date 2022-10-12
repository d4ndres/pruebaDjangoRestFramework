from rest_framework	import serializers
from django.contrib.auth.models import User

class UserSerializer( serializers.ModelSerializer ):
	class Meta:
		model = User
		fields = ('id','task_set', 'username')
		read_only_fields = ('id', 'username')

