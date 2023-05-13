# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    name = models.CharField(max_length=255)
    initials = models.CharField(max_length=2)
    update_general_rules = models.BooleanField(default=True)
    detection_systems = models.ManyToManyField('DetectionSystem', related_name='customers')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
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
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "DetectionSystem"
        
     
class Author(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "Authors"

class MitreTactic(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.id} - {self.name}"

class MitreTechnique(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    mitre_tactic = models.ForeignKey(MitreTactic, on_delete=models.CASCADE, related_name='mitre_techniques')
    def __str__(self):
        return f"{self.id} - {self.name}"
    
class Rule(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    mitre_tactics = models.ManyToManyField(MitreTactic,related_name='rules')
    mitre_techniques = models.ManyToManyField(MitreTechnique,related_name='rules')
    technologies = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name='rules')
    detection_systems = models.ManyToManyField(DetectionSystem, related_name='rules')
        
    def __str__(self):
        return self.name

    class Meta:
        db_table = "Rules"

