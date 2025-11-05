from django import forms

from .models import Profile

class LoginForm(forms.Form):

    username = forms.CharField(max_length=55,widget=forms.EmailInput(attrs={"class":"form-control form-control-lg",
                                                                            "placeholder":"Enter your email",
                                                                            "required":"required"                                                                        
                                                                           }))
    
    password = forms.CharField(max_length=55,widget=forms.PasswordInput(attrs={"class":"form-control form-control-lg",
                                                                            "placeholder":"Enter your password",
                                                                            "required":"required"                                                                        
                                                                           }))
    
class RegisterForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ["email","first_name","last_name","phone_num"]

        widgets = {

                'email' : forms.EmailInput(attrs={'class':'form-control','required':'required'}),

                'first_name' : forms.TextInput(attrs={'class':'form-control','required':'required'}),

                'last_name' : forms.TextInput(attrs={'class':'form-control','required':'required'}),

                'phone_num' : forms.TextInput(attrs={'class':'form-control','required':'required'}),

        }

        def clean(self):

            cleaned_data = super().clean()

            phone_num = cleaned_data.get("phone_num")

            if Profile.objects.filter(phone_num = phone_num).exists():

                self.add_error("phone_num","this phone is number already taken")

class OTPForm(forms.Form):

    email_otp = forms.CharField(max_length=6,widget=forms.TextInput(attrs={"class":"form-control form-control-lg",
                                                                            "placeholder":"Enter your email otp",
                                                                            "required":"required"                                                                        
                                                                           }))
    
class NewPasswordForm(forms.Form):

    password = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control form-control-lg",
                                                                                                                                                           
                                                                            "required":"required"                                                                        
                                                                           }))
    
    confirm_password = forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control form-control-lg",                                                                            
                                                                            "required":"required"                                                                        
                                                                           }))
    
    def clean(self) :

            cleaned_data = super().clean()

            password = cleaned_data.get("password")

            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                 
                 self.add_error("confirm_password","password missmatch")
    
    