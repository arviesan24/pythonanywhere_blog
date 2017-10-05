from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)  # compare user input from DB

            #****REMOVED GETTING AN ERROR FOR INCORRECT PASSWORD
            # if not user:  #give error if cant find user
            #     raise forms.ValidationError("User does not exist.")
            #
            # if not user.check_password(password):  #give error if password doesnt match
            #
            #
            # if not user.is_active:  #give error if user is inactive
            #     raise forms.ValidationError("This user is no longer active.")


            if user is not None:
                return super(UserLoginForm, self).clean(*args, **kwargs)  # if no errors return user

            else:
                raise forms.ValidationError("Incorrect username or password.")


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label="Email address")  #override the model form to require email
    email2 = forms.EmailField(label="Confirm Email")  #add additional field to confirm email
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    class Meta:
        model = User  #value from get_user_model()
        fields = [
            'username',
            'email',
            'email2',
            'password',
            'password2',
        ]

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered.")
        return email

    def clean_password2(self): #the name after the underscore must be same as fieldname (ex. clean_fieldname)
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Password confirmation doesn't match")
        return password