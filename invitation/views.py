from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from userprofile.models import Doctor
from .forms import MedicInvitationForm, FriendInvitationForm, RegistrationForm1, RegistrationForm2, RegistrationForm3
from .models import Invitation, FriendInvitation
from django.contrib.auth.models import User
from userprofile.forms import DoctorForm, UserForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from formtools.wizard.views import SessionWizardView


@staff_member_required
def invite_user(request):
    if request.method == 'POST':
        form = MedicInvitationForm(request.POST)
        if form.is_valid():

            invitation = Invitation(
                name=form.cleaned_data['name'],
                organization=form.cleaned_data['organization'],
                email=form.cleaned_data['email'],
                code="360MedNet" + User.objects.make_random_password(8)
            )
            if invitation.email and not User.objects.filter(email=invitation.email).exists():
                invitation.save()
                invitation.send_invite()
                messages.success(request,
                                 message='Invitation was successfully sent to %s.' %
                                         invitation.email
                                 )
            else:
                messages.error(request,
                               message='Invitation was not sent, %s is already registered with 360MedNet.' %
                                       invitation.email
                               )
    else:
        form = MedicInvitationForm()

    return render(request, 'invitation/user_invite.html', {'form': form})


def invite_friend(request):
    if request.method == 'POST':
        form = FriendInvitationForm(request.POST)
        if form.is_valid():

            friend_invitation = FriendInvitation(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                code=User.objects.make_random_password(8),
                sender=request.user
            )
            if friend_invitation.email and not User.objects.filter(email=friend_invitation.email).exists():
                friend_invitation.save()
                friend_invitation.send_invite()
                messages.success(request, 'Invitation sent')
            else:
                messages.error(request, 'Invitation not sent, email already registered with 360MedNet')
    else:
        form = FriendInvitationForm()

    return render(request, 'invitation/friend_invite.html', {'form': form})


def join(request, code):
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('/register_medic/')


def join_friend_invite(request, code):
    friend_invitation = get_object_or_404(FriendInvitation, code__exact=code)
    request.session['friend_invitation'] = friend_invitation.id
    return HttpResponseRedirect('/register_medic/')


def register_invited_user(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        doctor_form = DoctorForm(data=request.POST)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            doctor = doctor_form.save(commit=False)
            doctor.verification_status = True
            doctor.user = user
            doctor.save()
            if FriendInvitation.objects.filter(email=user.email).exists():
                FriendInvitation.objects.filter(email=user.email).update(accepted=True)
            else:
                Invitation.objects.filter(email=user.email).update(accepted=True)

            registered = True

        else:
            print(user_form.errors, doctor_form.errors)

    else:
        user_form = UserForm()
        doctor_form = DoctorForm()

    return render(request, 'userprofile/register.html', locals())


class RegistrationWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        # do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('formwizard/done.html')


def registration_one(request):
    initial = {'first_name': request.session.get('first_name', None),
               'last_name': request.session.get('last_name', None),
               'invitation_code': request.session.get('invitation_code', None)}
    form = RegistrationForm1(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data['first_name']
            request.session['last_name'] = form.cleaned_data['last_name']
            request.session['invitation_code'] = form.cleaned_data['invitation_code']
            return HttpResponseRedirect(reverse('reg_2'))
    return render(request, 'invitation/registration_one.html', {'form': form})


def registration_two(request):
    doctor_form = RegistrationForm3(request.POST or None)
    user_form = RegistrationForm2(request.POST or None)
    if request.method == 'POST':
        if doctor_form.is_valid() and user_form.is_valid():
            doctor = doctor_form.save(commit=False)
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            doctor = Doctor.objects.create(first_name=request.session['first_name'],
                                           last_name=request.session['last_name'],
                                           invitation_code=request.session['invitation_code'],
                                           invitation_code_object=Invitation.objects.
                                           get(code=request.session['invitation_code']),
                                           profession=doctor.profession,
                                           specialization=doctor.specialization, country=doctor.country, user=user,
                                           verification_status=True)

            # doctor.save()
            current_site = get_current_site(request)
            subject = 'Welcome to 360MedNet.'
            message = render_to_string('invitation/thank_you_signup_email.html', {
                'user': user,
                'doctor': doctor,
                'domain': current_site.domain,

            })
            to_email = user.email
            email = EmailMessage(subject, message, to=[to_email])
            email.content_subtype = "html"
            email.send()

            return HttpResponseRedirect(reverse('finished'))
    return render(request, 'invitation/registration_two.html', {'doctor_form': doctor_form, 'user_form': user_form})


def done(request):
    return render(request, 'invitation/done.html')