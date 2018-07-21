from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,get_user_model,login,logout

from .forms import UserLoginForm, UserRegisterForm

User = get_user_model()


# Create your views here.
def login_view(request):
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid(): 
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect("/posts")
    return render(request, "login_form.html", {"login_form": form, "title": title})


def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.is_active = False
        user.save()        
        if next:
            return redirect(next)
        return redirect("/posts")

    context = {
        "title": "Register",
        "register_form": form,
    }
    return render(request, "register_form.html", context)

def logout_view(request):
    logout(request)
    return redirect("/login")
