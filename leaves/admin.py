from django.contrib import admin
from .models import leavesDatabase,cumulativeLeavesDatabase,holidayList,delapprovedLeavesDatabase,approvedLeavesDatabase,appliedLeavesDatabase,todays_attendance2
from import_export import resources
from import_export.admin import ImportExportModelAdmin
import datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.admin import site
from django.db.models.query import QuerySet
    
# Register your models here.


class holidayDatabaseResource(resources.ModelResource):
    
    class Meta:
        model=holidayList

class holidayAdmin(ImportExportModelAdmin):
    list_display = ('date_today', 'type_of_holiday','status')
    fields = ('date_today','type_of_holiday')
    list_filter = ('date_today','type_of_holiday')
    search_fields = ('date_today','type_of_holiday')
    ordering = ('-date_today',)
    resource_class = holidayDatabaseResource
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    
    actions = ['update','delete_model']
    
    @admin.action(description='Delete the Selected Holiday List')
    def delete_model(self, request, obj):
        if not isinstance(obj, QuerySet):
            date_today = obj.date_today
            x = delapprovedLeavesDatabase.objects.filter(on_date = date_today)
            for i in x:
                id = i.id
                email = i.email
                leave_type = i.leave_type
                leave_duration = i.leave_duration
                temp = 0
                mor = get_object_or_404(leavesDatabase,email = email)
                
                if leave_duration == 'First Half' or leave_duration == 'Second Half':
                    temp = 0.5
                else:
                    temp = 1
                
                if leave_type == 'CL( Casual Leave )':
                    mor.total_available_cl = mor.total_available_cl - temp
                elif leave_type == 'PL( Privilege Leave )':
                    mor.total_available_pl = mor.total_available_pl - temp
                else:
                    mor.total_available_sl = mor.total_available_sl - temp
                mor.save()
                
                approvedLeavesDatabase.objects.get_or_create(
                    email = email,
                    Department = mor.Department,
                    Role = mor.Role,
                    leave_duration = leave_duration,
                    leave_type = leave_type,
                    on_date = i.on_date,
                    approved_on_date_time = i.approved_on_date_time,
                    approved_by = i.approved_by
                )
                
                delapprovedLeavesDatabase.objects.filter(id = id).delete()
            
            obj.delete()
        
        else:
            for ob in obj:
                date_today = ob.date_today
                x = delapprovedLeavesDatabase.objects.filter(on_date = date_today)
                for i in x:
                    id = i.id
                    email = i.email
                    leave_type = i.leave_type
                    leave_duration = i.leave_duration
                    temp = 0
                    mor = get_object_or_404(leavesDatabase,email = email)
                    
                    if leave_duration == 'First Half' or leave_duration == 'Second Half':
                        temp = 0.5
                    else:
                        temp = 1
                    
                    if leave_type == 'CL( Casual Leave )':
                        mor.total_available_cl = mor.total_available_cl - temp
                    elif leave_type == 'PL( Privilege Leave )':
                        mor.total_available_pl = mor.total_available_pl - temp
                    else:
                        mor.total_available_sl = mor.total_available_sl - temp
                    mor.save()
                    
                    approvedLeavesDatabase.objects.get_or_create(
                        email = email,
                        Department = mor.Department,
                        Role = mor.Role,
                        leave_duration = leave_duration,
                        leave_type = leave_type,
                        on_date = i.on_date,
                        approved_on_date_time = i.approved_on_date_time,
                        approved_by = i.approved_by
                    )
                    
                    delapprovedLeavesDatabase.objects.filter(id = id).delete()
                
                ob.delete()
            
    @admin.action(description='Update the Selected Holiday List')
    def update(modeladmin, request, queryset):
        for query in queryset:
            date_today = query.date_today
            x = approvedLeavesDatabase.objects.filter(on_date = date_today)
            for i in x:
                id = i.id
                email = i.email
                leave_type = i.leave_type
                leave_duration = i.leave_duration
                on_date = i.on_date
                temp = 0
                mor = get_object_or_404(leavesDatabase,email = email)
                
                if leave_duration == 'First Half' or leave_duration == 'Second Half':
                    temp = 0.5
                else:
                    temp = 1
                
                if leave_type == 'CL( Casual Leave )':
                    mor.total_available_cl = mor.total_available_cl + temp
                elif leave_type == 'PL( Privilege Leave )':
                    mor.total_available_pl = mor.total_available_pl + temp
                else:
                    mor.total_available_sl = mor.total_available_sl + temp
                mor.save()
                
                delapprovedLeavesDatabase.objects.get_or_create(
                    email = email,
                    Department = mor.Department,
                    Role = mor.Role,
                    leave_duration = leave_duration,
                    leave_type = leave_type,
                    on_date = on_date,
                    approved_on_date_time = i.approved_on_date_time,
                    approved_by = i.approved_by
                )
                approvedLeavesDatabase.objects.filter(id = id).delete()
                
            query.status = 'Updated'
            query.save()
            
    

admin.site.register(holidayList, holidayAdmin)    

    
class leavesDatabaseResource(resources.ModelResource):

    class Meta:
        model = leavesDatabase

class leavesDatabaseAdmin(ImportExportModelAdmin):
    list_display = ('email','Complete_Name')
    list_filter = ('email','Complete_Name')
    search_fields = ('email','Complete_Name')
    ordering = ('email',)
    resource_class = leavesDatabaseResource

admin.site.register(leavesDatabase, leavesDatabaseAdmin)

class appliedLeavesAdmin(admin.ModelAdmin):
    model = appliedLeavesDatabase
    list_display = ['id','email','leave_duration','on_date']
    
admin.site.register(appliedLeavesDatabase, appliedLeavesAdmin)

class approvedLeavesAdmin(admin.ModelAdmin):
    model = approvedLeavesDatabase
    list_display = ['id','email','leave_duration','on_date']
    
admin.site.register(approvedLeavesDatabase, approvedLeavesAdmin)

class delapprovedLeavesAdmin(admin.ModelAdmin):
    model = delapprovedLeavesDatabase
    list_display = ['id','email','leave_duration','on_date']
    
admin.site.register(delapprovedLeavesDatabase, delapprovedLeavesAdmin)

class cumulativeLeavesAdmin(admin.ModelAdmin):
    model = cumulativeLeavesDatabase
    list_display = ['id','email','Complete_Name','from_date','to_date','status']
    
admin.site.register(cumulativeLeavesDatabase, cumulativeLeavesAdmin)

# admin.site.register(cumulativeLeavesDatabase)
# admin.site.register(holidayList)
# admin.site.register(approvedLeavesDatabase)
# admin.site.register(appliedLeavesDatabase)
# admin.site.register(todays_attendance2)