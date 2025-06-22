from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import JobPost, Application
from .forms import UserRegistrationForm, JobPostForm, ApplicationForm
from rest_framework import viewsets
from .serializers import *
from rest_framework.permissions import AllowAny


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class JobPostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [AllowAny]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]


#  Different method for making controllers
# @api_view(["GET"])
# def getUser(request):
#     users = User.objects.all()
#     serialized = UserSerializer(users, many = True)
#     return Response(serialized.data)


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")


class JobPostListView(ListView):
    model = JobPost
    template_name = "job_list.html"
    context_object_name = "jobs"
    paginate_by = 5


class JobPostDetailView(DetailView):
    model = JobPost
    template_name = "job_detail.html"
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (
            self.request.user.is_authenticated
            and self.request.user == self.object.posted_by
        ):
            context["applications"] = self.object.application_set.all()
        return context


class JobPostCreateView(LoginRequiredMixin, CreateView):
    model = JobPost
    form_class = JobPostForm
    template_name = "job_post_create.html"
    success_url = reverse_lazy("job-list")

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "application_create.html"
    success_url = reverse_lazy("job-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_post"] = JobPost.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        form.instance.candidate = self.request.user
        job_post = JobPost.objects.get(pk=self.kwargs["pk"])
        form.instance.job_post = job_post
        return super().form_valid(form)
