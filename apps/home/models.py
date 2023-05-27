# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserPreferences(models.Model):
    THEME_CHOICES = [
        ('dark', 'Dark'),
        ('light', 'Light'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme_preference = models.CharField(max_length=20, choices=THEME_CHOICES, default='dark')
    
@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    if created:
        UserPreferences.objects.create(user=instance, theme_preference='dark')
        
class Customer(models.Model):
    name = models.CharField(max_length=255)
    initials = models.CharField(max_length=2)
    update_general_rules = models.BooleanField(default=True)
    detection_systems = models.ManyToManyField('DetectionSystem', related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='customers')
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = "Customers"

class DetectionSystem(models.Model):
    TYPE_CHOICES = (
        ('SIEM', 'SIEM'),
        ('EDR', 'EDR'),
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='detection_systems')
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
    class Meta:
        db_table = "DetectionSystem"

class MitreTactic(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mitre_tactics')
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'MitreTatics'
        verbose_name_plural = "MitreTatics"
        
    def __str__(self):
        return f"{self.id} - {self.name}"
        
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)


class MitreTechnique(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    mitre_tactics = models.ManyToManyField(MitreTactic, related_name='mitre_techniques')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='mitre_techniques')
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'MitreTechniques'
        verbose_name_plural = "MitreTechniques"

    def __str__(self):
        return f"{self.id} - {self.name}"
        
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)

class Technologies(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Technologies')
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'Technologies'
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='Tag')
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
    class Meta:
        db_table = 'Tags'

    def __str__(self):
        return self.name
    
class Rule(models.Model):
    
    SEVERITY_CHOICES = [
        ('Critical', 'Critical'),
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Informational', 'Informational'),
    ]
    
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    mitre_tactics = models.ManyToManyField(MitreTactic, related_name='rules')
    mitre_techniques = models.ManyToManyField(MitreTechnique, related_name='rules')
    technologies = models.ManyToManyField(Technologies, related_name='rules')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rules')
    modified_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='rules',blank=True)
    detection_systems = models.ManyToManyField(DetectionSystem, related_name='rules')
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()

        # Verificar si las técnicas están alineadas con las tácticas de MITRE
        for technique in self.mitre_techniques.all():
            tactic_ids = technique.mitre_tactics.values_list('id', flat=True)
            if self.mitre_tactics.filter(id__in=tactic_ids).exists():
                continue  # La técnica está alineada con al menos una táctica asociada a la regla
            raise ValidationError(f'The technique {technique.name} is not aligned with any of the MITRE tactics associated with the rule.')
    
    class Meta:
        db_table = "Rules"


        
class Watcher(models.Model):
    name = models.CharField(max_length=255)
    customers = models.ManyToManyField(Customer)
    detection_systems = models.ManyToManyField(DetectionSystem)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='watchers')
    technologies = models.ManyToManyField(Technologies, related_name='watchers')
    tags = models.ManyToManyField(Tag, related_name='watchers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()  

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
    class Meta:
        db_table = "Watchers"
        
class Report(models.Model):
    name = models.CharField(max_length=255)
    customers = models.ManyToManyField(Customer)
    detection_systems = models.ManyToManyField(DetectionSystem)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')
    technologies = models.ManyToManyField(Technologies, related_name='reports')
    tags = models.ManyToManyField(Tag, related_name='reports', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()  

    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Reports"
    
    