from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.db.models import Q
import datetime
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
# from employee.forms import EmployeeCreateForm
from leaves.models import *
from LMS.models import *
# from leave.forms import LeaveCreationForm
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta


# -------------------------------Dashboard Requirements--------------------------------

def dashboard(request):
	if not request.user.is_authenticated:
		return redirect('LMS:login_view')

	dataset = dict()
	Department = request.user.Department
	Role = request.user.Role
	num = 0
	approved_list = []
	total_list = []
	date_list = []
	mp1 = []
	mp2 = []
	date_check = datetime.date.today() + datetime.timedelta(days=1)
	if request.user.is_hod:
		employees = CustomUser.objects.filter(Department = Department,is_hod = False,is_director = False)
		num = employees.count()
		date_check = datetime.date.today() + datetime.timedelta(days=1)
		email = request.user.email
		labels = []
		count = [1, 10]
		date_list = []
		i = 0
		weekly_list = []
		months = {
			1: "JANUARY",
			2: "FEBRUARY",
			3: "MARCH",
			4: "APRIL",
			5: "MAY",
			6: "JUNE",
			7: "JULY",
			8: "AUGUST",
			9: "SEPTEMBER",
			10: "OCTOBER",
			11: "NOVEMBER",
			12: "DECEMBER"
		}
		m = 0
		month_list = []
		start_date = datetime.date.today()
		current_month = datetime.date.today().month
		current_year = datetime.date.today().year
		holidays = holidayList.objects.filter(Q(date_today__gte=start_date)).order_by('date_today')
		start_date = datetime.date(datetime.date.today().year, datetime.date.today().month, 1)
		end_date = start_date + relativedelta(day=31)
		leave_list = cumulativeLeavesDatabase.objects.filter(email = email).filter(
			Q(from_date__gte=start_date, from_date__lte=end_date) | Q(
				Q(to_date__gte=start_date, to_date__lte=end_date))).order_by('from_date').values()
		min_month = datetime.date(datetime.date.today().year - 1, 1, 1).strftime('%Y-%m')
		max_month = datetime.date(datetime.date.today().year, 12, 1).strftime('%Y-%m')
		name = request.user.Complete_Name
		shop = request.user.Department
		line = request.user.Role
		dataset = {
			'date_list': date_list,
			'month_list': month_list,
			'min_month': min_month,
			'max_month': max_month,
			'current_month_name': datetime.date.today().strftime('%Y-%m'),
			'leave_list': leave_list,
			'date_check': date_check,
			"email": email,
			'holidays' : holidays,
			"name":name,
			"shop":shop,
			"line":line,
			'labels': labels,
			'count': count,
			'employees':employees
		}
    
  
	elif request.user.is_director:
		employees = CustomUser.objects.filter(Department = Department,is_hod = False,is_director = False)
		num = employees.count()
		for i in range(1,8):
			date_list.append((datetime.date.today() + datetime.timedelta(days=i)))
			x = holidayList.objects.filter(date_today = (datetime.date.today() + datetime.timedelta(days=i)))
			if x.count():
				total_list.append('HOLIDAY')
				approved_list.append('HOLIDAY')
				mp1.append('HOLIDAY')
				mp2.append(x[0].type_of_holiday)
			else:
				mp1.append('')
				mp2.append('')
				temp1 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'First Half',Department = Department)
				temp2 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Second Half',Department = Department)
				temp3 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Full Day',Department = Department)
				k = (temp1.count()*0.5) + (temp2.count()*0.5) + (temp3.count())
				approved_list.append(k)
				if num != 0:
					total_list.append(round((k/num) * 100,2))
				else:
					total_list.append(0)
    
		dataset['lines'] = CustomUser.objects.filter(Department = Department).order_by('Role').distinct('Role')
		dataset['line'] = 'x'
		dataset['employees'] = employees
	
	# dataset['date_list'] = date_list
	dataset['num'] = num
	dataset['date_check'] = date_check
 
	return render(request,'dashboard/dashboard_index.html',dataset)



def linedashboard(request,id):
	if not request.user.is_authenticated:
		return redirect('LMS:login_view')
	
	dataset = dict()
	Department = request.user.Department
	Role = get_object_or_404(CustomUser,email = id).Role
	employees = CustomUser.objects.filter(Department = Department,Role = Role,is_hod = False,is_director = False)
	num = employees.count()
	approved_list = []
	total_list = []
	date_list = []
	mp1 = []
	mp2 = []
	for i in range(1,8):
		date_list.append((datetime.date.today() + datetime.timedelta(days=i)))
		x = holidayList.objects.filter(date_today = (datetime.date.today() + datetime.timedelta(days=i)))
		if x.count():
			total_list.append('HOLIDAY')
			approved_list.append('HOLIDAY')
			mp1.append('HOLIDAY')
			mp2.append(x[0].type_of_holiday)
		else:
			mp1.append('')
			mp2.append('')
			temp1 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'First Half',Department = Department,Role= Role)
			temp2 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Second Half',Department = Department,Role= Role)
			temp3 = approvedLeavesDatabase.objects.filter(on_date = (datetime.date.today() + datetime.timedelta(days=i)),leave_duration = 'Full Day',Department = Department,Role= Role)
			k = (temp1.count()*0.5) + (temp2.count()*0.5) + (temp3.count())
			approved_list.append(k)
			if num != 0:
				total_list.append(round((k/num) * 100,2))
			else:
				total_list.append(0)
   
	dataset['mp1'] = mp1
	dataset['mp2'] = mp2
	dataset['lines'] = CustomUser.objects.filter(Department = Department).order_by('Role').distinct('Role')
	dataset['employees'] = employees
	dataset['line'] = Role
	dataset['approved_list'] = approved_list
	dataset['day1'] = total_list[0]
	dataset['day2'] = total_list[1]
	dataset['day3'] = total_list[2]
	dataset['day4'] = total_list[3]
	dataset['day5'] = total_list[4]
	dataset['day6'] = total_list[5]
	dataset['day7'] = total_list[6]
	dataset['date_list'] = date_list
	dataset['num'] = num
 
	return render(request,'dashboard/dashboard_index.html',dataset)





# --------------------------------------Employee Listing-----------------------------------

def dashboard_employees(request):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	
	if request.user.is_hod:
		Role = request.user.Role
		Department = request.user.Department
		dataset['shop'] = Department
		dataset['line'] = Role
		dataset['employee_list'] = CustomUser.objects.filter(Department = Department,is_hod = False,is_director = False).order_by('Complete_Name')

	if request.user.is_director:
		dataset['employee_list'] = CustomUser.objects.filter(is_hod = False,is_director = False,is_staff=False).order_by('Department','Complete_Name')
		dataset['lines'] = CustomUser.objects.all().order_by('Department').distinct('Department')
		dataset['line'] = 'x'
	dataset['title'] = "Men_On_Roll"
	
	return render(request,'dashboard/employee_app.html',dataset)


def employeesfilter(request,id):
	if not (request.user.is_authenticated and request.user.is_director):
		return redirect('/logout')

	dataset = dict()
	# Department = request.user.Department
	Department = get_object_or_404(CustomUser,email = id).Department

	# dataset['shop'] = Department
	
	dataset['employee_list'] = CustomUser.objects.filter(Department=Department,is_hod = False,is_director = False,is_staff= False).order_by('Complete_Name')
		
	dataset['title'] = "Men_On_Roll"
	dataset['lines'] = CustomUser.objects.all().order_by('Department').distinct('Department')
	dataset['line'] = Department
		
	return render(request,'dashboard/employee_app.html',dataset)



# -----------------------------Dashboard And Leave View----------------------------------

def dashboard_employee_info(request,email):
	if not request.user.is_authenticated:
		return redirect('/logout')
	
	employee = get_object_or_404(CustomUser, email = email)
	email = email
	# quota = get_object_or_404(leavesDatabase,email = email)
	
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(email = email,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1)))
	name = get_object_or_404(CustomUser,email = email).Complete_Name
 
	dataset = dict()
	dataset['employee'] = employee
	# dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['email'] = email
 
	return render(request,'dashboard/employee_detail.html',dataset)



def leaves_view(request,id):
	if not (request.user.is_authenticated):
		return redirect('/login')

	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	email = leave.email
	employee = get_object_or_404(CustomUser,email = email)
	# quota = get_object_or_404(leavesDatabase,email = email)
	x = ""
	if leave.status == 0:
		x = 'Waiting'
	elif leave.status == 1:
		x = 'Approved'
	else:
		x = 'Rejected'
  
	return render(request,'dashboard/leave_detail_view.html',{'leave':leave,'employee':employee,'title':'{0}-{1} leave'.format(leave.Complete_Name,x)})





# # ---------------------LEAVES LISTING-------------------------------------------


def leaves_list(request):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	
	if request.user.is_hod:
		Department = request.user.Department
		leaves = cumulativeLeavesDatabase.objects.all_leaves()
		dataset['leave_list'] = leaves.filter(Department = Department,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).exclude(Role = 'HOD').order_by('from_date')
	
	elif request.user.is_director:
		leaves = cumulativeLeavesDatabase.objects.all_leaves()
		dataset['leave_list'] = leaves.filter(from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		dataset['x'] = 'All'
	dataset['title'] = 'All_Leaves'
	return render(request,'dashboard/leaves_recent.html',dataset)


def leaves_list_filter(request,id):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	x = ''
	if request.user.is_hod:
		Department = request.user.Department
		leaves = cumulativeLeavesDatabase.objects.all_leaves()
		dataset['leave_list'] = leaves.filter(Department = Department,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).exclude(Role = 'HOD').order_by('from_date')
	
	elif request.user.is_director:
		if id == 'All' or id == None:
			leaves = cumulativeLeavesDatabase.objects.all_leaves()
			x = 'All'
		elif id == '0':
			leaves = cumulativeLeavesDatabase.objects.filter(Role = 'HOD')
			x = 'HOD'
		elif id == '1':
			leaves = cumulativeLeavesDatabase.objects.all().exclude(Role = 'HOD')
			x = 'staff'
    
		dataset['leave_list'] = leaves.filter(from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		dataset['x'] = x
	dataset['title'] = 'All_Leaves'
	return render(request,'dashboard/leaves_recent.html',dataset)



def pending_leaves_list(request):
	if not (request.user.is_authenticated):
		return redirect('/login')

	dataset = dict()
	
	if request.user.is_hod:
		Department = request.user.Department
		leaves = cumulativeLeavesDatabase.objects.all_pending_leaves()
		dataset['leave_list'] = leaves.filter(Department = Department,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).exclude(Role = 'HOD').order_by('from_date')
		
	elif request.user.is_director:
		leaves = cumulativeLeavesDatabase.objects.all_pending_leaves()
		dataset['leave_list'] = leaves.filter(from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		dataset['x'] = 'All'
  
	dataset['title'] = 'Waiting_Leaves'
	return render(request,'dashboard/leaves_pending.html',dataset)

def pending_leaves_list_filter(request,id):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	x = ''
	if request.user.is_hod:
		Department = request.user.Department
		leaves = cumulativeLeavesDatabase.objects.all_leaves()
		dataset['leave_list'] = leaves.filter(Department = Department,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).exclude(Role = 'HOD').order_by('from_date')
	
	elif request.user.is_director:
		if id == 'All' or id == None:
			leaves = cumulativeLeavesDatabase.objects.filter(status="0")
			x = 'All'
		elif id == '0':
			leaves = cumulativeLeavesDatabase.objects.filter(Role = 'HOD',status="0")
			x = 'HOD'
		elif id == '1':
			leaves = cumulativeLeavesDatabase.objects.filter(status="0").exclude(Role = 'HOD')
			x = 'staff'
    
		dataset['leave_list'] = leaves.filter(from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		dataset['x'] = x
	dataset['title'] = 'All_Leaves'
	return render(request,'dashboard/leaves_pending.html',dataset)

def leaves_approved_list(request):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	leaves = cumulativeLeavesDatabase.objects.all_approved_leaves()
 
	if request.user.is_hod:
		Department = request.user.Department
		dataset['leave_list'] = leaves.filter(Department = Department,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).exclude(Role = 'HOD').order_by('from_date')
	elif request.user.is_director:
		dataset['leave_list'] = leaves.filter(from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		dataset['x'] = 'All'
  
	dataset['title'] = 'Approved_Leaves'
	return render(request,'dashboard/leaves_approved.html',dataset)

def approved_leaves_list_filter(request,id):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	x = ''
	if request.user.is_hod:
		Department = request.user.Department
		leaves = cumulativeLeavesDatabase.objects.all_leaves()
		dataset['leave_list'] = leaves.filter(Department = Department,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).exclude(Role = 'HOD').order_by('from_date')
	
	elif request.user.is_director:
		if id == 'All' or id == None:
			leaves = cumulativeLeavesDatabase.objects.filter(status="1")
			x = 'All'
		elif id == '0':
			leaves = cumulativeLeavesDatabase.objects.filter(Role = 'HOD',status="1")
			x = 'HOD'
		elif id == '1':
			leaves = cumulativeLeavesDatabase.objects.filter(status="1").exclude(Role = 'HOD')
			x = 'staff'
    
		dataset['leave_list'] = leaves.filter(from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		dataset['x'] = x
  
	dataset['title'] = 'All_Leaves'
	return render(request,'dashboard/leaves_approved.html',dataset)

def leave_rejected_list(request):
	if not (request.user.is_authenticated):
		return redirect('/logout')
	dataset = dict()
	leaves = cumulativeLeavesDatabase.objects.all_rejected_leaves()
	
	if request.user.is_hod:
		Department = request.user.Department
		dataset['leaves_list_rejected'] = leaves.filter(Department = Department,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).exclude(Role = 'HOD').order_by('from_date')
	elif request.user.is_director:
		leaves = leaves.filter(from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
		dataset['leaves_list_rejected'] = leaves
		dataset['x'] = 'All'
  
	dataset['title'] = 'Rejected_Leaves'
	return render(request,'dashboard/rejected_leaves_list.html',dataset)


def leave_rejected_list_filter(request,id):
	if not (request.user.is_authenticated):
		return redirect('/logout')

	dataset = dict()
	x = ''
	if request.user.is_hod:
		Department = request.user.Department
		leaves = cumulativeLeavesDatabase.objects.all_leaves()
		dataset['leaves_list_rejected'] = leaves.filter(Department = Department,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).exclude(Role = 'HOD').order_by('from_date')
	
	elif request.user.is_director:
		if id == 'All' or id == None:
			leaves = cumulativeLeavesDatabase.objects.filter(status="2")
			x = 'All'
		elif id == '0':
			leaves = cumulativeLeavesDatabase.objects.filter(Role = 'HOD',status="2")
			x = 'HOD'
		elif id == '1':
			leaves = cumulativeLeavesDatabase.objects.filter(status="2").exclude(Role = 'HOD')
			x = 'staff'
		dataset['x'] = x
   
		dataset['leaves_list_rejected'] = leaves.filter(from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	
	dataset['title'] = 'All_Leaves'
	return render(request,'dashboard/rejected_leaves_list.html',dataset)




# ----------------------------Personal Leaves Sorting----------------------------------


def sortedleaves(request,email):
	if not (request.user.is_hod or request.user.is_director):
		return redirect('/logout')

	employee = get_object_or_404(CustomUser, email=email)
	email = email
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(email = email,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	name = get_object_or_404(CustomUser,email = email).Complete_Name
 
	
	# quota = get_object_or_404(leavesDatabase,email = email)
 
	dataset = dict()
	dataset['employee'] = employee
	# dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['email'] = email
 
	return render(request,'dashboard/employee_detail.html',dataset)



def personalapproved(request,email):
	if not (request.user.is_hod or request.user.is_director):
		return redirect('/login')
	employee = get_object_or_404(CustomUser, email = email)
	email = email
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(email = email,status = 1,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	name = get_object_or_404(CustomUser,email = email).Complete_Name
	
	# quota = get_object_or_404(leavesDatabase,email = email)
 
	dataset = dict()
	dataset['employee'] = employee
	# dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['email'] = email

	return render(request,'dashboard/employee_detail.html',dataset)


def personalwaiting(request,email):
	if not (request.user.is_hod or request.user.is_director):
		return redirect('/login')
	employee = get_object_or_404(CustomUser, email = email)
	email = email
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(email = email,status = 0,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	name = get_object_or_404(CustomUser,email = email).Complete_Name
	# quota = get_object_or_404(leavesDatabase,email = email)
 
	dataset = dict()
	dataset['employee'] = employee
	# dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['email'] = email
 
	return render(request,'dashboard/employee_detail.html',dataset)

def personalrejected(request,email):
	if not (request.user.is_hod or request.user.is_director):
		return redirect('/login')
	employee = get_object_or_404(CustomUser, email = email)
	email = email
	leaves = cumulativeLeavesDatabase.objects.all_leaves()
	leaves = leaves.filter(email = email,status = 2,from_date__gte=(datetime.date.today() + datetime.timedelta(days=1))).order_by('from_date')
	name = get_object_or_404(CustomUser,email = email).Complete_Name
	# quota = get_object_or_404(leavesDatabase,email = email)
 
	dataset = dict()
	dataset['employee'] = employee
	# dataset['quota'] = quota
	dataset['title'] = 'profile - {0}'.format(employee.Complete_Name)
	dataset['leave_list'] = leaves
	dataset['name'] = name
	dataset['email'] = email

	return render(request,'dashboard/employee_detail.html',dataset)







# ------------------------------------Action on Leaves--------------------------------------

def unapprove_leave(request,id):
	if not (request.user.is_authenticated and (request.user.is_hod or request.user.is_director)):
		return redirect('/login')

	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	email = leave.email
	
	leave.reason = ''
	leave.action_by = request.user.Complete_Name
	leave.unapprove_leave
 
	return redirect('dashboard:leaveslist') 



def approve_leave(request,id):
	if not ((request.user.is_hod or request.user.is_director) and request.user.is_authenticated):
		return redirect('/login')
	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
      
	leave.reason = ''
	Complete_Name = request.user.Complete_Name
	leave.action_by = Complete_Name
	leave.approve_leave
	
	return redirect('dashboard:leaveslist')


def reject_leave(request,id):
	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	reason = request.GET.get('reason')
	leaveType = leave.leave_type
	leave.reason = reason
	leave.action_by = request.user.Complete_Name
	leave.reject_leave
 

	if request.user.is_director:
		x = 1
	else:
		x = 2
	data = {'x': x}
 
	return JsonResponse(data)


def unreject_leave(request,id):
	if not (request.user.is_hod or request.user.is_director):
		return redirect('/logout')
	leave = get_object_or_404(cumulativeLeavesDatabase, id = id)
	leave.reason = ''
	leave.action_by = request.user.Complete_Name
	leave.unreject_leave
	messages.success(request,'Leave is now in Pending list ',extra_tags = 'alert alert-success alert-dismissible show')
 
	return redirect('dashboard:leaveslist')




