from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .models import User, Department, Position
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

#Display Home Page
def index(request):
    return render(request,'users/index.html')

#Display User Tables
def user_table(request):
    user_list = User.objects.all().order_by('-id')
    user_list_total =  User.objects.all()
    department_list = Department.objects.all()

    paginator = Paginator(user_list, 5)
    page_number = request.GET.get('page')
    users_paginated = paginator.get_page(page_number)

    context = {'page_obj':users_paginated,'department_list':department_list,'user_list_total':user_list_total}
    return render(request,'users/user_table.html',context)

#Display Login Page
def login_page(request):
    return render(request,'users/login.html')

def process_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:

        login(request,user)
        return HttpResponseRedirect('/users')
    
    else:
        return render(request,'users/login.html',{'error_message':"Login Failed"})
    
def process_logout(request):
    logout(request)
    return HttpResponseRedirect('/users/login_page')
    
@login_required(login_url = '/users/login_page')
#Display Add user
def add_user(request):
    department_list = Department.objects.order_by('department_id')
    position_list = Position.objects.order_by('position_id')
    context = {'department_list':department_list, 'position_list':position_list}
    return render(request,'users/add_user.html',context)


#Process Add User
def process_add_user(request):
    user_fname = request.POST.get('user_fname')
    user_lname = request.POST.get('user_lname')
    user_email = request.POST.get('user_email')
    user_department_name = request.POST.get('user_department')
    user_position_name = request.POST.get('user_position')

    # Fetch the department and position instances
    user_department = get_object_or_404(Department, department_name=user_department_name)
    user_position = get_object_or_404(Position, position_name=user_position_name)

    # Default profile image if not provided
    if request.FILES.get('user_image'):
        user_image = request.FILES.get('user_image')
    else:
        user_image = 'user_image/user_default_image.jpg'

    try:
        # Check if user already exists
        User.objects.get(user_email=user_email)
        department_list = Department.objects.order_by('department_id')
        position_list = Position.objects.order_by('position_id')
        return render(request, 'users/add_user.html', {
            'error_message': 'User Email already exists.',
            'department_list': department_list,
            'position_list': position_list,
        })
    except ObjectDoesNotExist:
        # Create the user only if all required fields are present
        user = User.objects.create(
            user_fname=user_fname, 
            user_lname=user_lname, 
            user_email=user_email, 
            user_department=user_department,  # Assign the Department instance
            user_position=user_position,      # Assign the Position instance
            user_image=user_image
        )
        user.save()
    messages.success(request, 'User added successfully!')
    return HttpResponseRedirect('/users/')

def add_department(request):
    return render(request,'users/add_department.html')

#Process Add Department
def process_add_department(request):
    department_name = request.POST.get('department_name')

    try:
        # Check if user already exists
        Department.objects.get(department_name=department_name)
       
        return render(request, 'users/add_department.html', {
            'error_message': 'Department already exists.',
        })
    except ObjectDoesNotExist:
        # Create the user only if all required fields are present
        department = Department.objects.create(
            department_name=department_name, 
        )
        department.save()
    messages.success(request, 'Department added successfully!')
    return HttpResponseRedirect('/users/')
    


@login_required(login_url = '/users/login_page')
def user_detail(request,user_id):
    try:
        user= User.objects.get(pk=user_id)

        context = {'user':user}

    except User.DoesNotExist:
        raise Http404('User does not exist')
    
    return render(request, 'users/user_detail.html',context)

@login_required(login_url = '/users/login_page')
def edit_user(request, user_id):
    try:
        user= User.objects.get(pk=user_id)
        department_list = Department.objects.order_by('department_id')
        position_list = Position.objects.order_by('position_id')

        context = {'user':user,'department_list':department_list,'position_list':position_list}


    except User.DoesNotExist:
        raise Http404('User does not exist')
    
    return render(request, 'users/edit_user.html',context)

def process_edit_user(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    user_image = request.FILES.get('user_image')

    try:
        user_fname = request.POST.get('user_fname')
        user_lname = request.POST.get('user_lname')
        user_email = request.POST.get('user_email')
        user_department_name = request.POST.get('user_department')
        user_position_name = request.POST.get('user_position')

        # Fetch the department and position instances
        user_department = get_object_or_404(Department, department_name=user_department_name)
        user_position = get_object_or_404(Position, position_name=user_position_name)


    except(KeyError,User.DoesNotExist):
        return render(request, 'users/user_detail.html',{
            'user':user,
            'error_message':"Problem Updating User Record",
        })
    
    else:
        updated_user = User.objects.get(pk=user_id)
        updated_user.user_fname = user_fname
        updated_user.user_lname = user_lname
        updated_user.user_email = user_email
        updated_user.user_department = user_department
        updated_user.user_position = user_position
        if user_image:
            updated_user.user_image = user_image
        updated_user.save()
        messages.success(request, 'User updated successfully!')
        return HttpResponseRedirect(reverse('users:user detail',args=(user_id,)))

def delete_user(request,user_id):
    User.objects.filter(id=user_id).delete()
    messages.success(request, 'User deleted successfully!')
    return HttpResponseRedirect('/users/')


def search_user(request):
    user_list_total = User.objects.all().order_by('-id')
    department_list = Department.objects.all()
    
    term = request.GET.get('search','')
    user_list = User.objects.filter(Q(user_fname__icontains=term)|Q(user_lname__icontains=term)).order_by('-id')
    paginator = Paginator(user_list,5)
    page_number = request.GET.get('page')
    user_list = paginator.get_page(page_number)
    

    return render(request,'users/user_table.html',{'page_obj':user_list,'department_list':department_list,
                                                   'user_list_total':user_list_total})
