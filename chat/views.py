from django.shortcuts import render, redirect
from .models import Thread, Message
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count
# Create your views here.




# authentications

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hashes the password
        if commit:
            user.save()
        return user


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'chat/signup.html'
    success_url = reverse_lazy('index')  # Redirect to the chat page after successful signup
    def form_valid(self, form):
        response = super().form_valid(form)
        # You can log the user in automatically after signup if you want
        login(self.request, self.object)  
        return response

def index(request):
    user = request.user
    personal_threads = Thread.objects.filter(users=user, thread_type='PSN')
    group_threads= Thread.objects.filter(users=user, thread_type='GRP')
    users_in_threads = User.objects.filter(chat_users__in=personal_threads).exclude(id=user.id).distinct()
    users_not_in_threads = User.objects.exclude(id__in=users_in_threads)
    context = {'personal_threads': personal_threads, 'group_threads':group_threads, 'strangers':users_not_in_threads }
    print(users_not_in_threads)
    return render(request, "chat/index.html", context)

def room(request, room_id):
    if not request.user.is_authenticated:
        return redirect("login-user")
    friend = User.objects.get(id=room_id) 
    print(friend.email, "our friend")
    thread = Thread.objects.annotate(num_users=Count('users')).filter(thread_type='PSN', users=request.user).filter(users=friend,num_users=2
).first()
    Message.objects.filter(thread=thread, read=False).update(read=True)
    messages = Message.objects.filter(thread=thread)
    return render(request, "chat/room.html", {'room_id': room_id, 'messages': messages, 'friend': friend})