# -*- encoding: utf-8 -*-


from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Customer, DetectionSystem, Rule, MitreTactic, MitreTechnique, Watcher, Report, Technologies, Tag, UserPreferences
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from .forms import RuleForm
from django.http import JsonResponse

class UserPreferencesInline(admin.StackedInline):
    model = UserPreferences
    can_delete = False
    verbose_name_plural = "User preferences"

class UserAdmin(BaseUserAdmin):
    inlines = [UserPreferencesInline]

class CustomerForm(forms.ModelForm):
    update_general_rules = forms.ChoiceField(choices=((True, 'Yes'), (False, 'No')))

    class Meta:
        model = Customer
        fields = '__all__'
        
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
    list_display = ('id', 'name', 'initials', 'detection_systems_display', 'update_general_rules', 'created_by', 'created_at', 'modified_at')

    def detection_systems_display(self, obj):
        return ", ".join([t.name for t in obj.detection_systems.all()])
    detection_systems_display.short_description = "Detection Systems"
    
class MitreTacticAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by','created_at', 'modified_at')

class TechonologiesAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by','created_at', 'modified_at')
    
class TagsAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by','created_at', 'modified_at')
    
class MitretechniqueAdminList(admin.ModelAdmin):
    list_display = ('id', 'name', 'mitre_tactics_display', 'created_by', 'created_at', 'modified_at')

    def mitre_tactics_display(self, obj):
        tactic_names = ", ".join([tactic.name for tactic in obj.mitre_tactics.all()])
        return tactic_names

    mitre_tactics_display.short_description = "MITRE Tactics"


class DetectionSystemList(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'created_by','created_at', 'modified_at')
    
class RuleList(admin.ModelAdmin):
    list_display = ('id', 'name', 'severity', 'mitre_tactics_display', 'mitre_techniques_display', 'technologies_display', 'tags_display', 'created_by', 'detection_systems_display', 'created_at','modified_at')
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
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Obtener el contexto existente
        extra_context = extra_context or {}

        # Verificar si se realizó una solicitud POST (se envió el formulario)
        if request.method == 'POST':
            # Obtener el valor de las tácticas seleccionadas
            selected_tactics = request.POST.getlist('tactics')

            # Realizar la lógica para obtener las técnicas según las tácticas seleccionadas
            # ...
            
            # Devolver las técnicas en formato JSON
            data = [{'id': technique.id, 'name': technique.name} for technique in techniques]
            return JsonResponse(data, safe=False)

        # Agregar el script JavaScript al contexto existente
        extra_context['admin_script'] = """
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script>
            $(document).ready(function() {
                $('#id_tactics').change(function() {
                    var selectedTactics = $(this).val();

                    // Realizar una solicitud AJAX para obtener las técnicas según las tácticas seleccionadas
                    $.ajax({
                        url: window.location.href,
                        type: 'POST',
                        data: {'tactics': selectedTactics},
                        success: function(response) {
                            // Limpiar el campo de selección de técnicas
                            $('#id_techniques').empty();

                            // Agregar las nuevas opciones de técnicas al campo de selección
                            for (var i = 0; i < response.length; i++) {
                                var technique = response[i];
                                $('#id_techniques').append('<option value="' + technique.id + '">' + technique.name + '</option>');
                            }
                        },
                        error: function(xhr, textStatus, errorThrown) {
                            console.log('Error:', errorThrown);
                        }
                    });
                });
            });
            </script>
        """

        # Llamar al método original de la superclase para renderizar el formulario
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

class WatcherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'customers_display', 'detection_systems_display', 'technologies_display', 'tags_display', 'created_at', 'modified_at')

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
admin.site.register(User, UserAdmin)
