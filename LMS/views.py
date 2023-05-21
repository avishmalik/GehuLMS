from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm,UserShopAddForm,UserSuperAddForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse



def home(request):
    return render(request,'home.html')

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email = email,password=password)
            if user is not None and user.is_staff:
                login(request,user)
                return HttpResponseRedirect(reverse('admin:index'))
            elif user is not None and user.is_member:
                login(request,user)
                return redirect('leaves:searchLeavesData')
            elif user is not None and (user.is_hod):
                login(request,user)
                return redirect('dashboard:dashboard')
            elif user is not None and (user.is_director):
                login(request,user)
                return redirect('dashboard:leaveslist')
            else:
                msg = 'Invalid Credentials'
        else:
            msg = 'Error Validating Form'
    return render(request,'login.html',{'form' : form, 'msg': msg})


def register_user_view(request):
	# WORK ON (MESSAGES AND UI) & extend with email field
    if request.method == 'POST':
        if request.user.is_director:
            form = UserShopAddForm(data = request.POST)
            if form.is_valid():
                instance = form.save(commit = False)
                # instance.Department = request.user.Department
                instance.save()
                Complete_Name = form.cleaned_data.get("Complete_Name")

                messages.success(request,'Account created for {0} !!!'.format(Complete_Name),extra_tags = 'alert alert-success alert-dismissible show' )
                return redirect('LMS:register')
            else:
                messages.error(request,'Username or password is invalid',extra_tags = 'alert alert-warning alert-dismissible show')
                return redirect('LMS:register')
        else:
            form = UserSuperAddForm(data = request.POST)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.Department = request.user.Department
                # instance.Role = request.user.Role
                instance.save()
                Complete_Name = form.cleaned_data.get("Complete_Name")

                messages.success(request,'Account created for {0} !!!'.format(Complete_Name),extra_tags = 'alert alert-success alert-dismissible fade show' )
                return redirect('LMS:register')
            else:
                messages.error(request,'Username or password is invalid',extra_tags = 'alert alert-warning alert-dismissible fade show')
                return redirect('LMS:register')
            
    if request.user.is_director:
        form = UserShopAddForm()
    else:
        form = UserSuperAddForm()
    dataset = dict()
    dataset['form'] = form
    dataset['title'] = 'register users'
    return render(request,'accounts/register.html',dataset)


def changepassword(request):
	if not request.user.is_authenticated:
		return redirect('/login')
	'''
	Please work on me -> success & error messages & style templates
	'''
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			update_session_auth_hash(request,user)

			messages.success(request,'Password changed successfully',extra_tags = 'alert alert-success alert-dismissible show' )
			return redirect('LMS:changepassword')
		else:
			messages.error(request,'Error,changing password',extra_tags = 'alert alert-warning alert-dismissible show' )
			return redirect('LMS:changepassword')
			
	form = PasswordChangeForm(request.user)
	return render(request,'accounts/change_password_form.html',{'form':form,'user':request.user})



def logout_view(request):
    logout(request)
    return redirect('LMS:login_view')


def bluecollar(request):
    return render(request,'leaveDataDisplay.html')

def hod(request):
    return render(request,'dashboard/dashboard_index.html')