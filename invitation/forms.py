from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from invitation.models import Invitation, FriendInvitation
from userprofile.models import Doctor


class MedicInvitationForm(forms.ModelForm):
    name = forms.CharField(label='Invitee Name')
    organization = forms.CharField(label='Invitee Organization')
    email = forms.EmailField(label='Invitee Email')

    class Meta:
        model = Invitation
        fields = ('name', 'organization', 'email')


class FriendInvitationForm(forms.ModelForm):
    name = forms.CharField(label='Invitee Name')
    email = forms.EmailField(label='Invitee Email')

    class Meta:
        model = FriendInvitation
        fields = ('name', 'email')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Create Password")
    username = forms.CharField(help_text=False)
    email = forms.EmailField(label="Email address")

    layout = Layout(Row('email', 'username', 'password')

                    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class DoctorForm(forms.ModelForm):
    layout = Layout(Fieldset('Personal details',
                             'profession', 'country'
                             ))

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'profession', 'country')


def invitation_code_exists(value):
    invitee = Invitation.objects.filter(code=value).exists()
    if not invitee:
        raise forms.ValidationError("The invitation code provided does not exist. Please verify the code you have "
                                    "entered with the one sent to your email")


class RegistrationForm1(forms.ModelForm):
    invitation_code = forms.CharField(max_length=17, validators=[invitation_code_exists])
    layout = Layout(Row('first_name', 'last_name', ),
                    'invitation_code'

                    )

    class Meta:
        model = Doctor
        fields = ('first_name', 'last_name', 'invitation_code')


class RegistrationForm2(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Create Password")
    username = forms.CharField(help_text=False)
    email = forms.EmailField(label="Email Address")
    layout = Layout(email,
                    username, password

                    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class RegistrationForm3(forms.ModelForm):
    country = forms.CharField(label="Country of Practice")
    layout = Layout(
        Fieldset('Medical details',
                 'profession', 'country'
                 ))

    class Meta:
        model = Doctor
        fields = ('profession', 'country')


class RegistrationForm4(forms.Form):
    tos = forms.BooleanField(required=True, label="Click here to indicate that you have read and agree to the "
                                                  "360MedNet Terms of use and Privacy Policy",
                             )
