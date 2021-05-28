from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from user.models import UserProfile
from home.models import Setting
from product.models import Category
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'userprofile'}
    return render(request, 'user_profile.html', context)


def logout_view(request):
    logout(request)
    request.session['table_no'] = None
    request.session['order_id'] = None
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['table_no'] = None
            request.session['order_id'] = None
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Your username or password is incorrect.")
            return HttpResponseRedirect('/login')
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'login'}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password1 = request.POST['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            request.session['table_no'] = None
            request.session['order_id'] = None
            return HttpResponseRedirect('/')

    form = SignUpForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'form': form, 'page': 'login'}
    return render(request, 'signup.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        setting = Setting.objects.get(pk=1)
        current_user = request.user
        if current_user.id is not None:
            profile = UserProfile.objects.get(user_id=current_user.id)
        else:
            profile = None
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'setting': setting,
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile,
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        setting = Setting.objects.get(pk=1)
        category = Category.objects.all()
        current_user = request.user
        if current_user.id is not None:
            profile = UserProfile.objects.get(user_id=current_user.id)
        else:
            profile = None
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
            'category': category,
            'setting': setting,
            'profile': profile,
        }
        return render(request, 'user_password.html', context)