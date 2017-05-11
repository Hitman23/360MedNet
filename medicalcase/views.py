from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import MedicalCase, MedicalCaseCategory
from userprofile.models import Doctor
from .forms import MedicalCaseForm
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView


class MedicalCaseCreate(CreateView):
    model = MedicalCase
    form = MedicalCaseForm
    #fields = "__all__"
    fields = ['title', 'chief_complaint', 'patient_age', 'patient_gender', 'patient_country_of_origin',
              'history_of_present_illness', 'medical_history', 'surgical_history', 'social_history', 'family_history',
              'allergies', 'medications', 'review_of_systems', 'physical_examination', 'diagnostic_tests',
              'medical_case_category']

    success_url = '/feed/'
    template_name = 'medicalcase/medicalcase_form.html'

    def form_valid(self, form):
        form.instance.doctor = Doctor.objects.get(user=self.request.user)
        form.instance.save()
        return super(MedicalCase, self).form_valid(form)


def medical_case_list(request):
    medical_cases = MedicalCase.list_medical_cases()

    return render(request, 'post/feeds.html', locals())
