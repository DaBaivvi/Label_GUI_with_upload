from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse


#Introduction
def introduction(request):
    return render(request, 'introduction.html')

## Login view
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # 获取 'next' 参数，如果没有，则重定向到 'label' 页面
                next_url = request.GET.get('next', 'label')  
                return redirect(next_url)  # 登录成功，重定向到 label 页面
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
                return redirect('login')  # 登录失败，返回登录页面
    
        return render(request, 'login.html')  # 假设 'login.html' 是你的登录模板
    else:
        return redirect('label') 



def redirect_to_login(request):
    messages.info(request, 'Please log in to access the upload and label pages.')
    return redirect('login')


#Logout
def logout_view(request):
    next_url = request.GET.get('next', '/')
    request.session.flush()
    logout(request)
    return redirect(next_url)


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            # 创建新用户并保存到数据库
            new_user = User.objects.create_user(username=username, email=email, password=password)

            # 获取登录页面的 URL
            login_url = reverse('login')
            return JsonResponse({'status': 'success', 'username': username, 'next': login_url})
        else:
            # 获取表单错误信息
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'errors': errors})
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})
