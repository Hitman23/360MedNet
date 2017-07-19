from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import MedicalCase, MedicalCaseCategory, Comment
from userprofile.models import Doctor
from .forms import MedicalCaseForm
from django.views.generic.edit import DeleteView, ModelFormMixin
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, MedicalCaseSearchForm
from django.core.urlresolvers import reverse_lazy, reverse


class MedicalCaseCreate(CreateView):
    model = MedicalCase
    form_class = MedicalCaseForm

    success_url = '/medical_cases/'
    template_name = 'medicalcase/medicalcase_form.html'

    def form_valid(self, form):
        form.instance.doctor = Doctor.objects.get(user=self.request.user)
        form.instance.save()
        return super(MedicalCaseCreate, self).form_valid(form)


class MedicalCaseList(ListView):
    model = MedicalCase
    form_class = MedicalCaseSearchForm
    paginate_by = 5
    context_object_name = 'casses'
    template_name = 'medicalcase/medicalcase_list.html'

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            return MedicalCase.objects.filter(medical_case_category__icontains=
                                              form.cleaned_data['medical_case_category'])
        return MedicalCase.objects.all()


# def search_medicalcases(request):
#     form = MedicalCaseSearchForm
#     if request.method == 'GET':
#         if form.is_valid():
#             return MedicalCase.objects.filter(medical_case_category__icontains=
#                                               form.cleaned_data['medical_case_category'])


class MedicalCaseDetail(ModelFormMixin, DetailView):
    model = MedicalCase
    form_class = CommentForm

    def get_success_url(self):
        return reverse('medical_case-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(MedicalCaseDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def comments(self):
        return Comment.objects.filter(medical_case=MedicalCase.objects.get(pk=self.object.pk)).all().order_by(
            '-created_at')


@login_required
def medical_case_comment_add_view(request, pk):
    form = CommentForm(request.POST or None)

    if form.is_valid() and pk:
        form.instance.doctor = Doctor.objects.get(user=request.user)
        form.instance.medical_case = MedicalCase.objects.get(pk=pk)
        form.save()
        return HttpResponseRedirect(reverse('medical_case-detail', kwargs={'pk': pk}))
    return HttpResponseRedirect(reverse('medical_case-detail', kwargs={'pk': pk}))
