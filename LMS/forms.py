from django.contrib.auth.forms import UserCreationForm,UserChangeForm

from .models import CustomUser
from django import forms

 
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                "class" : "form-control",
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class" : "form-control",
            }
        )
    
    )

class UserShopAddForm(UserCreationForm):
	'''
	Extending UserCreationForm - with email

	'''

	class Meta:
		model = CustomUser
		fields = ['email','Complete_Name','password1','password2','Department','Role','is_active']
		

class UserSuperAddForm(UserCreationForm):
	'''
	Extending UserCreationForm - with email

	'''

	class Meta:
		model = CustomUser
		fields = ['email','Complete_Name','password1','Role','password2','is_active']
		
	

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)