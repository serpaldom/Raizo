# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib import admin
from .models import Customer, DetectionSystem, Author, Rule, MitreTactic, MitreTechnique
from django.db.models.signals import post_save
from django.dispatch import receiver

from django import forms

class CustomerForm(forms.ModelForm):
    update_general_rules = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')))

    class Meta:
        model = Customer
        fields = '__all__'
        
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ('id', 'name', 'initials', 'detection_systems_display', 'update_general_rules', 'created_at')

    def detection_systems_display(self, obj):
        return ", ".join([t.name for t in obj.detection_systems.all()])
    detection_systems_display.short_description = "Detection Systems"
    
class MitreTacticAdminList(admin.ModelAdmin):
    list_display = ('id', 'name')
    
class MitretechniqueAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'mitre_tactic_display')

    def mitre_tactic_display(self, obj):
        return f"{obj.mitre_tactic.id} - {obj.mitre_tactic.name}"

    mitre_tactic_display.short_description = "MITRE Tactic"


class DetectionSystemList(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'created_at')
    
class AuthorList(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    
class RuleList(admin.ModelAdmin):
    list_display = ('id', 'name', 'mitre_tactics_display', 'mitre_techniques_display', 'technologies', 'tags', 'author', 'detection_systems_display', 'created_at')

    def mitre_tactics_display(self, obj):
        return ", ".join([f"{t.id}-{t.name}" for t in obj.mitre_tactics.all()])

    mitre_tactics_display.short_description = "MITRE Tactics"

    def mitre_techniques_display(self, obj):
        return ", ".join([f"{t.id}-{t.name}" for t in obj.mitre_techniques.all()])

    mitre_techniques_display.short_description = "MITRE Techniques"

    def detection_systems_display(self, obj):
        return ", ".join([t.name for t in obj.detection_systems.all()])
    
    detection_systems_display.short_description = "Detection Systems"

        
@receiver(post_save, sender=Customer)
def apply_rule_to_new_customer(sender, instance, created, **kwargs):
    if created and instance.update_general_rules and instance.detection_systems.exists():
        detection_systems = instance.detection_systems.all()
        for detection_system in detection_systems:
            detection_system_rules = Rule.objects.filter(detection_systems=detection_system)
            general_rule = detection_system_rules.filter(rule_type='GENERAL').first()
            if general_rule:
                general_rule.customers.add(instance)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(DetectionSystem, DetectionSystemList)
admin.site.register(Author, AuthorList)
admin.site.register(Rule, RuleList)
admin.site.register(MitreTactic, MitreTacticAdminList)
admin.site.register(MitreTechnique,MitretechniqueAdminList)
