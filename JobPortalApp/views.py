from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import JobPost, Application
from .forms import UserRegistrationForm, JobPostForm, ApplicationForm
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import S3ImageUploader


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
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})


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


# Image Upload API endpoints
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """Upload image to AWS S3"""
    if "image" not in request.FILES:
        return Response(
            {"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    image_file = request.FILES["image"]
    folder = request.data.get("folder", "images/")

    # Initialize S3 uploader
    uploader = S3ImageUploader()

    # Upload image
    result = uploader.upload_image(image_file, folder)

    if result["success"]:
        return Response(
            {
                "message": "Image uploaded successfully",
                "url": result["url"],
                "key": result["key"],
                "filename": result["filename"],
            },
            status=status.HTTP_201_CREATED,
        )
    else:
        return Response({"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_image(request):
    """Delete image from AWS S3"""
    s3_key = request.data.get("key")

    if not s3_key:
        return Response(
            {"error": "S3 key is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Initialize S3 uploader
    uploader = S3ImageUploader()

    # Delete image
    result = uploader.delete_image(s3_key)

    if result["success"]:
        return Response(
            {"message": "Image deleted successfully"}, status=status.HTTP_200_OK
        )
    else:
        return Response({"error": result["error"]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_multiple_images(request):
    """Upload multiple images to AWS S3"""
    if "images" not in request.FILES:
        return Response(
            {"error": "No image files provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    images = request.FILES.getlist("images")
    folder = request.data.get("folder", "images/")

    if len(images) > 10:  # Limit to 10 images
        return Response(
            {"error": "Maximum 10 images allowed"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Initialize S3 uploader
    uploader = S3ImageUploader()

    results = []
    errors = []

    for image in images:
        result = uploader.upload_image(image, folder)
        if result["success"]:
            results.append(
                {
                    "filename": result["filename"],
                    "url": result["url"],
                    "key": result["key"],
                }
            )
        else:
            errors.append({"filename": image.name, "error": result["error"]})

    return Response(
        {
            "message": f"{len(results)} images uploaded successfully",
            "uploaded": results,
            "errors": errors,
        },
        status=status.HTTP_201_CREATED if results else status.HTTP_400_BAD_REQUEST,
    )
