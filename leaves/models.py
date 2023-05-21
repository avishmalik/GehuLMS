from django.db import models
from django.utils.translation import gettext as _
from .manager import LeaveManager
# Create your models here.
import datetime


class leavesDatabase(models.Model):
    email = models.EmailField(null=False)
    # card_no = models.CharField(max_length=100, null=False)
    Complete_Name = models.CharField(max_length=80)
    Department = models.CharField(max_length=100, null=True)
    Role = models.CharField(max_length=100, null=True)
    total_assigned_pl = models.FloatField(default=0)
    total_assigned_cl = models.FloatField(default=0)
    total_assigned_sl = models.FloatField(default=0)
    total_available_pl = models.FloatField(default=0)
    total_available_cl = models.FloatField(default=0)
    total_available_sl = models.FloatField(default=0)

class cumulativeLeavesDatabase(models.Model):
    email = models.EmailField(null=False)
    Complete_Name = models.CharField(max_length=80)
    Department = models.CharField(max_length=100, null=True)
    Role = models.CharField(max_length=100, null=True)
    leave_type = models.CharField(max_length=100, null=False)
    leave_duration = models.CharField(max_length=100, null=False)
    from_date = models.DateField(auto_now=False,auto_now_add=False,null=False)
    applied_on_date = models.DateField(auto_now=False,auto_now_add=True,null=True)
    to_date = models.DateField(auto_now=False,auto_now_add=False,null=False)
    status = models.IntegerField(default=0)
    reason = models.CharField(max_length=255,default = "")
    action_by = models.CharField(max_length=80,default="")
    
    
    objects = LeaveManager()
    
    class Meta:
        verbose_name = _('Leave')
        verbose_name_plural = _('Leaves')
        ordering = ['-applied_on_date']
        
    @property
    def leave_days(self):
        startdate = self.from_date
        enddate = self.to_date
        dates = 0
        if startdate > enddate:
            return 
        if self.leave_duration == 'Half Day':
            dates = 0.5
            return dates
        else: 
            dates = (enddate - startdate) + datetime.timedelta(days=1)
        return dates.days

        
    @property
    def leave_approved(self):       
        return self.status == 1




    @property
    def approve_leave(self):
        if not self.status == 1:
            self.status = 1
            self.save()




    @property
    def unapprove_leave(self):
        if not self.status == 0:
            self.status = 0
            self.save()


    @property
    def reject_leave(self):
        if self.status == 0 or  self.status == 1:
            self.status = 2
            self.save()

    @property
    def unreject_leave(self):
        if self.status == 2:
            self.status = 0
            self.save()

    @property
    def is_rejected(self):
        return self.status == 2
    

class approvedLeavesDatabase(models.Model):
    email = models.EmailField(null=False)
    Department = models.CharField(max_length=100, null=False)
    Role = models.CharField(max_length=100, null=False)
    leave_duration = models.CharField(max_length=100, null=False)
    leave_type = models.CharField(max_length=100, null=False)
    on_date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    approved_on_date_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    approved_by = models.CharField(max_length=100, null=True)
    
class delapprovedLeavesDatabase(models.Model):
    email = models.EmailField(null=False)
    Department = models.CharField(max_length=100, null=False)
    Role = models.CharField(max_length=100, null=False)
    leave_duration = models.CharField(max_length=100, null=False)
    leave_type = models.CharField(max_length=100, null=False)
    on_date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    approved_on_date_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    approved_by = models.CharField(max_length=100, null=True)

class appliedLeavesDatabase(models.Model):
    email = models.EmailField(null=False)
    Department = models.CharField(max_length=100, null=False)
    Role = models.CharField(max_length=100, null=False)
    leave_duration = models.CharField(max_length=100, null=False)
    leave_type = models.CharField(max_length=100, null=False)
    on_date = models.DateField(auto_now=False, auto_now_add=False, null=False)
    applied_on_date_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)


class holidayList(models.Model):
    date_today = models.DateField(auto_now=False, auto_now_add=False, null=False)
    type_of_holiday = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length = 20,default = 'Not Updated')
    
class todays_attendance2(models.Model):
    sno = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100, blank=True,db_index=True)
    p_time = models.CharField(max_length=100, blank=True)
    date_t = models.DateField(auto_now_add = False, auto_now=False,blank=True)
    submission = models.CharField(max_length=200, null=True)
    sym_issue = models.CharField(max_length=200, null=True)
    containment_issue = models.CharField(max_length=200, null=True)
    quarantine_issue = models.CharField(max_length=200, null=True)
    submission_from_company = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    dep = models.CharField(max_length=200, null=True)