
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# from .models import Person,SuperV
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .forms import CustomUserCreationForm,CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin,ImportExportModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','is_staff','Complete_Name','Department','Role','is_member','is_hod','is_director')
    list_filter = ('email','is_staff','Complete_Name','Department','Role','is_member','is_hod','is_director')
    fieldsets = (
        (None,{'fields': ('email','password','Complete_Name','Department','Role','is_member','is_hod','is_director')}),
        ('Permissions', {'fields': ('is_staff','is_active',)}),
    )
    
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields' : ('email','password1','password2','is_staff','is_active','Complete_Name','Department','Role','is_member','is_hod','is_director')}
        ),
    )
    search_fields = ('email','Complete_Name')
    ordering = ('email',)




# admin.site.register(CustomUser,CustomUserAdmin)

# class UserResource(resources.ModelResource):
#     class Meta:
#         model = CustomUser
#         # fields = ('id','email','Complete_Name','Department','Role')
#         list_display = ('id','email','Complete_Name','Department','Role')

# class UserAdmin(ImportExportModelAdmin,UserAdmin):
#     resource_class = UserResource
#     pass

# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)


# class PersonResource(resources.ModelResource):

#     class Meta:
#         model = Person

# class PersonAdmin(ImportExportModelAdmin):
#     list_display = ('id','email','Complete_Name','Department','Role')
#     resource_class = PersonResource

# admin.site.register(Person, PersonAdmin)

# class SuperVAdmin(admin.ModelAdmin):
#     list_display = ('email','Complete_Name','Department','Role')
    
# admin.site.register(SuperV,SuperVAdmin)






