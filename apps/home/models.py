# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from simple_history.models import HistoricalRecords

class Customer(models.Model):
    name = models.CharField(max_length=255)
    initials = models.CharField(max_length=2)
    update_general_rules = models.BooleanField(default=True)
    detection_systems = models.ManyToManyField('DetectionSystem', related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_customers')
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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_detection_systems')
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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_mitre_tactics')
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.id} - {self.name}"
        
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
class MitreTechnique(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    mitre_tactic = models.ForeignKey(MitreTactic, on_delete=models.CASCADE, related_name='mitre_techniques')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_mitre_techniques')
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.id} - {self.name}"
        
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)

class Rule(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    mitre_tactics = models.ManyToManyField(MitreTactic,related_name='rules')
    mitre_techniques = models.ManyToManyField(MitreTechnique,related_name='rules')
    technologies = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_rules')
    modified_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=255)
    detection_systems = models.ManyToManyField(DetectionSystem, related_name='rules')
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if self.created_by and not self.created_by.is_staff:
            raise PermissionDenied("Only staff members can create customers")
        super().save(*args, **kwargs)
    class Meta:
        db_table = "Rules"
class Watcher(models.Model):
    name = models.CharField(max_length=255)
    customers = models.ManyToManyField(Customer)
    detection_systems = models.ManyToManyField(DetectionSystem)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()  

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Watchers"
        
class Report(models.Model):
    name = models.CharField(max_length=255)
    customers = models.ManyToManyField(Customer)
    detection_systems = models.ManyToManyField(DetectionSystem)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()  

    def __str__(self):
        return self.name