from django import forms
from django_select2.forms import Select2MultipleWidget
from .models import Rule, MitreTechnique, Technologies, Customer
from django.contrib.admin.widgets import FilteredSelectMultiple

class RuleForm(forms.ModelForm):
    mitre_techniques = forms.ModelMultipleChoiceField(
        queryset=MitreTechnique.objects.all(),
        widget=FilteredSelectMultiple('MITRE Techniques', is_stacked=False),
    )
    technologies = forms.ModelMultipleChoiceField(
        queryset=Technologies.objects.all(),
        widget=FilteredSelectMultiple('Technologies', is_stacked=False),
    )

    class Meta:
        model = Rule
        fields = '__all__'
        
class CustomerForm(forms.ModelForm):
    update_general_rules = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')))

    class Meta:
        model = Customer
        fields = '__all__'
