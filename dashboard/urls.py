from django.urls import path
from .import views


app_name = 'dashboard'

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    # path('shop/',views.shopdashboard,name='shopdashboard'),
    path('shopline/<int:id>',views.linedashboard,name='linedashboard'),
    path('employeesfilter/<str:id>',views.employeesfilter,name='employeesfilter'),
    path('employees/all/',views.dashboard_employees,name='employees'),
    # path('welcome/',views.dashboard,name='dashboard'),

    # # Employee
    # path('shopemployees/all/',views.dashboard_shopemployees,name='shopemployees'),
    # path('employee/create/',views.dashboard_employees_create,name='employeecreate'),
    path('employee/profile/<str:email>/',views.dashboard_employee_info,name='employeeinfo'),
    # path('employee/profile/edit/<int:id>/',views.employee_edit_data,name='edit'),

    # # # Emergency
    # # path('emergency/create/',views.dashboard_emergency_create,name='emergencycreate'),
    # # path('emergency/update/<int:id>',views.dashboard_emergency_update,name='emergencyupdate'),

    # # # Family
    # # path('family/create/',views.dashboard_family_create,name='familycreate'),
    # # path('family/edit/<int:id>',views.dashboard_family_edit,name='familyedit'),
    
    # # #Bank
    # # path('bank/create/',views.dashboard_bank_create,name='bankaccountcreate'),
    
    # #---work-on-edit-view------#
    # # path('bank/edit/<int:id>/',views.employee_bank_account_update,name='accountedit'),
    # path('leave/apply/',views.leave_creation,name='createleave'),
    path('leaves/all/',views.leaves_list,name='leaveslist'),
    path('leaves/all/<str:id>',views.leaves_list_filter,name='leaveslistfilter'),
    # path('shopleaves/all/',views.shopleaves_list,name='shopleaveslist'),
    path('personaleaves/all/<str:email>',views.sortedleaves,name='sortedleaves'),
    path('personalapproved/all/<str:email>',views.personalapproved,name='personalapproved'),
    path('leaves/personalwaiting/<str:email>',views.personalwaiting,name='personalwaiting'),
    path('leaves/personalrejected/<str:email>',views.personalrejected,name='personalrejected'),
    path('leaves/pending/',views.pending_leaves_list,name='pendingleaveslist'),
    path('leaves/pending/<str:id>',views.pending_leaves_list_filter,name='pendingleaveslistfilter'),
    # path('shopleaves/pending/',views.shoppending_leaves_list,name='shoppendingleaveslist'),
    path('leaves/approved/all/',views.leaves_approved_list,name='approvedleaveslist'),
    path('leaves/approved/<str:id>',views.approved_leaves_list_filter,name='approvedleaveslistfilter'),
    # path('shopleaves/approved/all/',views.shopleaves_approved_list,name='shopapprovedleaveslist'),
    # path('leaves/cancel/all/',views.cancel_leaves_list,name='canceleaveslist'),
    path('leaves/all/view/<int:id>/',views.leaves_view,name='userleaveview'),
    # path('leaves/view/table/',views.view_my_leave_table,name='staffleavetable'),
    path('leave/approve/<int:id>/',views.approve_leave,name='userleaveapprove'),
    path('leave/unapprove/<int:id>/',views.unapprove_leave,name='userleaveunapprove'),
    # path('leave/cancel/<int:id>/',views.cancel_leave,name='userleavecancel'),
    # path('leave/uncancel/<int:id>/',views.uncancel_leave,name='userleaveuncancel'),
    path('leaves/rejected/all/',views.leave_rejected_list,name='leavesrejected'),
    path('leaves/rejected/<str:id>/',views.leave_rejected_list_filter,name='leavesrejectedfilter'),
    # path('shopleaves/rejected/all/',views.shopleave_rejected_list,name='shopleavesrejected'),
    path('leave/reject/<int:id>/',views.reject_leave,name='reject'),
    path('leave/unreject/<int:id>/',views.unreject_leave,name='unreject'),
    # BIRTHDAY ROUTE
    # path('birthdays/all/',views.birthday_this_month,name='birthdays'),



]
