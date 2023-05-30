# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Customer, DetectionSystem, Rule, MitreTactic, MitreTechnique, Watcher, Report, Technologies, Tag, UserPreferences, Exceptions
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from .forms import RuleForm, CustomerForm, CustomUserCreationForm, ExceptionsForm

class UserPreferencesInline(admin.StackedInline):
    model = UserPreferences
    can_delete = False
    verbose_name_plural = "User preferences"

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    inlines = [UserPreferencesInline]
        
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ('id', 'name', 'initials', 'detection_systems_display', 'created_by', 'created_at', 'modified_at')
    list_filter = ('name', 'created_by','created_at', 'modified_at')
    search_fields = ['name']

    def detection_systems_display(self, obj):
        return ", ".join([t.name for t in obj.detection_systems.all()])
    detection_systems_display.short_description = "Detection Systems"
    
class MitreTacticAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by','created_at', 'modified_at')
    list_filter = ('id', 'name', 'created_by','created_at', 'modified_at')
    search_fields = ['name']

class TechonologiesAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by','created_at', 'modified_at')
    list_filter = ('name', 'created_by','created_at', 'modified_at')
    search_fields = ['name']
    
class TagsAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by','created_at', 'modified_at')
    list_filter = ('name', 'created_by','created_at', 'modified_at')
    search_fields = ['name']
    
class MitretechniqueAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'mitre_tactics_display', 'created_by', 'created_at', 'modified_at')
    search_fields = ['name']

    def mitre_tactics_display(self, obj):
        tactic_names = ", ".join([tactic.name for tactic in obj.mitre_tactics.all()])
        return tactic_names

    mitre_tactics_display.short_description = "MITRE Tactics"


class DetectionSystemList(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'created_by','created_at', 'modified_at')
    list_filter = ('id', 'name', 'type', 'created_by','created_at', 'modified_at')
    search_fields = ['name']
    
class RuleList(admin.ModelAdmin):
    list_display = ('id', 'name', 'severity', 'mitre_tactics_display', 'mitre_techniques_display', 'technologies_display', 'tags_display', 'created_by', 'detection_systems_display', 'created_at','modified_at')
    list_filter = ('id','name','severity', 'created_at', 'modified_at')
    search_fields = ['name']
    form = RuleForm
    def mitre_tactics_display(self, obj):
        tactic_names = ", ".join([tactic.name for tactic in obj.mitre_tactics.all()])
        return tactic_names

    mitre_tactics_display.short_description = "MITRE Tactics"

    def mitre_techniques_display(self, obj):
        technique_names = ", ".join([f"{technique.id} - {technique.name}" for technique in obj.mitre_techniques.all()])
        return technique_names

    mitre_techniques_display.short_description = "MITRE Techniques"

    def detection_systems_display(self, obj):
        return ", ".join([t.name for t in obj.detection_systems.all()])
    
    detection_systems_display.short_description = "Detection Systems"

    def technologies_display(self, obj):
        return ", ".join([t.name for t in obj.technologies.all()])
    
    technologies_display.short_description = "Technologies"

    def tags_display(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    tags_display.short_description = "Tags"

class WatcherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'customers_display', 'detection_systems_display', 'technologies_display', 'tags_display', 'created_at', 'modified_at')
    list_filter = ('name', 'created_at', 'modified_at')
    search_fields = ['name']

    def customers_display(self, obj):
        return ", ".join([c.name for c in obj.customers.all()])
    
    customers_display.short_description = "Customers"

    def detection_systems_display(self, obj):
        return ", ".join([d.name for d in obj.detection_systems.all()])
    
    detection_systems_display.short_description = "Detection Systems"
    
    def technologies_display(self, obj):
        return ", ".join([t.name for t in obj.technologies.all()])
    
    technologies_display.short_description = "Technologies"

    def tags_display(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    tags_display.short_description = "Tags"

class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'customers_display', 'detection_systems_display', 'technologies_display', 'tags_display', 'created_at', 'modified_at')
    list_filter = ('name', 'created_at', 'modified_at')
    search_fields = ['name']

    def customers_display(self, obj):
        return ", ".join([c.name for c in obj.customers.all()])
    
    customers_display.short_description = "Customers"

    def detection_systems_display(self, obj):
        return ", ".join([d.name for d in obj.detection_systems.all()])
    
    detection_systems_display.short_description = "Detection Systems"

    def technologies_display(self, obj):
        return ", ".join([t.name for t in obj.technologies.all()])
    
    technologies_display.short_description = "Technologies"

    def tags_display(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    
    tags_display.short_description = "Tags"
    
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_id', 'action_flag']
    search_fields = ['user']

class ExceptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'rule', 'get_detection_systems', 'get_customers', 'created_at', 'modified_at')
    list_filter = ('rule', 'detection_system', 'created_at', 'modified_at')
    search_fields = ('rule__name', 'detection_system__name', 'customers__name')
    readonly_fields = ('created_at', 'modified_at')
    verbose_name_plural = "Exceptions"
    form = ExceptionsForm

    def get_customers(self, obj):
        return ", ".join([customer.name for customer in obj.customers.all()])
    
    def get_detection_systems(self, obj):
        return ", ".join([detection_system.name for detection_system in obj.detection_system.all()])

    get_customers.short_description = 'Customers'
    get_detection_systems.short_description = 'Detection System'
    

     
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
admin.site.register(Rule, RuleList)
admin.site.register(MitreTactic, MitreTacticAdminList)
admin.site.register(MitreTechnique,MitretechniqueAdminList)
admin.site.register(Watcher, WatcherAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Technologies, TechonologiesAdminList)
admin.site.register(Tag, TagsAdminList)
admin.site.register(Session)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.unregister(User)
admin.site.register(UserPreferences)  
admin.site.register(User, UserAdmin)
admin.site.register(Exceptions,ExceptionsAdmin)  

