from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from .models import MedicalCase, Comment, MedicalCaseCategory


class MedicalCaseForm(forms.ModelForm):

    # medical_case_category = forms.ModelMultipleChoiceField(queryset=MedicalCaseCategory.objects.all(), required=True,
    #                                                        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = MedicalCase

        fields = ('title', 'chief_complaint','patient_age', 'patient_gender', 'patient_country_of_origin',
                  'history_of_present_illness', 'medical_history', 'surgical_history', 'social_history',
                  'family_history', 'allergies', 'medications', 'review_of_systems', 'physical_examination',
                  'diagnostic_tests', 'any_other_details', 'medical_case_category', 'purpose', 'image')


class CommentForm(forms.ModelForm):
    comment_content = forms.CharField(label='Comment', widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('comment_content',)


class MedicalCaseSearchForm(forms.ModelForm):
    class Meta:
        model = MedicalCase

        fields = ('medical_case_category',)
