from django import forms
from .models import Rule, MitreTechnique, Technologies, Customer
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from .models import UserPreferences, Exceptions, DetectionSystem
from django.contrib.auth.models import User
class ExceptionsForm(forms.ModelForm):
    detection_system = forms.ModelMultipleChoiceField(
    queryset=DetectionSystem.objects.all(),
    widget=FilteredSelectMultiple('Detection System', is_stacked=False),
    )
    customers = forms.ModelMultipleChoiceField(
        queryset=Customer.objects.all(),
        widget=FilteredSelectMultiple('Customers', is_stacked=False),
    )

    class Meta:
        model = Exceptions
        fields = '__all__'
        widgets = {
            'artifact': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Separate multiple artifacts with commas.'}),
        }

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
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserPreferences.objects.create(user=user, theme_preference='dark')
        return user

