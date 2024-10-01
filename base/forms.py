from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants', 'updated', 'created']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'username', 'email', 'bio']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
        exclude = ['updated', 'created']