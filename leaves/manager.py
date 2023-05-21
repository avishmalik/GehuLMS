from django.db import models
import datetime




class LeaveManager(models.Manager):
	# Department = request.user.Department
	# Role = request.user.Role
    
	def get_queryset(self):
		'''
		overrides objects.all() 
		return all leaves including pending or approved
		'''
		return super().get_queryset()

	def all_leaves(self):
		return super().get_queryset().order_by('-applied_on_date')

	def all_pending_leaves(self):
		'''
		gets all pending leaves -> Leave.objects.all_pending_leaves()
		'''
		return super().get_queryset().filter(status = 0).order_by('-applied_on_date')# applying FIFO 


	def all_rejected_leaves(self):
		return super().get_queryset().filter(status = 2).order_by('-applied_on_date')




	def all_approved_leaves(self):
		'''
		gets all approved leaves -> Leave.objects.all_approved_leaves()
		'''
		return super().get_queryset().filter(status = 1).order_by('-applied_on_date')



	def current_year_leaves(self):
		'''
		returns all leaves in current year; Leave.objects.all_leaves_current_year()
		or add all_leaves_current_year().count() -> int total 
		this include leave approved,pending,rejected,cancelled

		'''
		return super().get_queryset().filter(startdate__year = datetime.date.today().year)



