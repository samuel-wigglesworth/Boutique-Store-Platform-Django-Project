from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import CustomerProfileForm, SignUpForm
from .models import CustomerProfile


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("dashboard:home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile_view(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = CustomerProfileForm(instance=profile)
    return render(request, "accounts/profile.html", {"form": form})
from django.shortcuts import render

# Create your views here.
