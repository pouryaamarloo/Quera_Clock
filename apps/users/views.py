from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
from .forms import RegisterForm ,ProfileForm
from apps.users.forms import RegisterForm
from django.contrib.auth import login


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("users:profile")

    def form_valid(self, form):
        user =form.save()
        login(self.request , user)
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self):
        return self.request.user
