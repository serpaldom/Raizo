# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Customer, DetectionSystem, Rule
from django.contrib.auth.models import User
import csv
from django.shortcuts import redirect

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if load_template == 'index.html':
            total_customers = Customer.objects.count()
            total_users = User.objects.count()
            total_detection_systems = DetectionSystem.objects.count()
            total_rules = Rule.objects.count()
            
            context['total_customers'] = total_customers
            context['total_users'] = total_users
            context['total_detection_systems'] = total_detection_systems
            context['total_rules'] = total_rules
        
        if load_template == 'tables-customers.html':
            customers = Customer.objects.all()
            
            context['customers'] = customers
        
        if load_template == 'tables-detection_systems.html':
            detection_systems = DetectionSystem.objects.all()
            
            context['detection_systems'] = detection_systems
            
        if request.path.split('/')[1] == 'export':
            object_to_export = request.path.split('/')[-1]
            if object_to_export == 'customers':
                customers = Customer.objects.all()
                response = HttpResponse(
                    content_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="customers.csv"'},
                )

                writer = csv.writer(response)
                # CSV columns
                writer.writerow(['ID', 'Name', 'Initials', 'Detection systems', 'Created by', 'Created at (UTC)','Modified at (UTC)'])
                for customer in customers:
                    detection_systems = ', '.join([ds.name for ds in customer.detection_systems.all()])
                    writer.writerow([customer.id, customer.name, customer.initials, detection_systems,customer.created_by, customer.created_at, customer.modified_at])
                # Return the response
                return response
            
            elif object_to_export == 'detection_systems':
                detection_systems = DetectionSystem.objects.all()
                response = HttpResponse(
                    content_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="detection_systems.csv"'},
                )

                writer = csv.writer(response)
                # CSV columns
                writer.writerow(['ID', 'Name', 'Type', 'Customers', 'Created by', 'Created at (UTC)','Modified at (UTC)'])
                for detection_system in detection_systems:
                    customers = ', '.join([customer.name for customer in detection_system.customers.all()])
                    writer.writerow([detection_system.id, detection_system.name, detection_system.type, customers, detection_system.created_by, detection_system.created_at, detection_system.modified_at])
                # Return the response
                return response
            
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
