# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from .models import Customer, DetectionSystem, Rule, Watcher, Report
from django.contrib.auth.models import User
import csv
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta, date
from django.contrib.admin.models import LogEntry
from django.db.models.functions import ExtractMonth



@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return redirect("/index.html")
    #return HttpResponse(html_template.render(context, request))


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
            # Obtener la fecha y hora actual
            now = timezone.now()

            # Obtener las fechas límite para el último día, últimos 7 días y último mes
            last_day = now - timedelta(days=1)
            last_week = now - timedelta(days=7)
            last_month = now - timedelta(days=30)
            
            # Get the start date of the current week
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            try:
                total_customers = Customer.objects.count()
                total_users = User.objects.count()
                total_detection_systems = DetectionSystem.objects.count()
                total_rules = Rule.objects.count()
                total_watchers = Watcher.objects.count()
                total_reports = Report.objects.count()
            except:
                total_customers = 0
                total_users = 0
                total_detection_systems = 0
                total_rules = 0
                total_watchers = 0
                total_reports = 0
            
            try:
                # Obtener los 3 usuarios que han creado la mayor cantidad de Rule en el último día
                top_users_last_day = User.objects.annotate(total_rules=Count('created_rules')).filter(
                    created_rules__created_at__gte=last_day
                ).order_by('-total_rules')[:5]

                # Obtener los 3 usuarios que han creado la mayor cantidad de Rule en los últimos 7 días
                top_users_last_week = User.objects.annotate(total_rules=Count('created_rules')).filter(
                    created_rules__created_at__gte=last_week
                ).order_by('-total_rules')[:5]

                # Obtener los 3 usuarios que han creado la mayor cantidad de Rule en el último mes
                top_users_last_month = User.objects.annotate(total_rules=Count('created_rules')).filter(
                    created_rules__created_at__gte=last_month
                ).order_by('-total_rules')[:5]
            except:
                top_users_last_day = 0
                top_users_last_week = 0
                top_users_last_month = 0

            try:
                # Obtener el número de reglas por día de la semana actual
                rules_by_day_of_week = Rule.objects.filter(created_at__gte=start_of_week).values('created_at__week_day').annotate(count=Count('id')).order_by('created_at__week_day')

                # Crear un diccionario para almacenar el recuento de reglas por día
                rules_count_by_day = {day: 0 for day in range(1, 8)}

                # Actualizar el diccionario con los valores reales
                for rule in rules_by_day_of_week:
                    day = rule['created_at__week_day']
                    count = rule['count']
                    rules_count_by_day[day] = count

                # Crear una lista con los valores de reglas por día en orden
                rules_by_day_list = [rules_count_by_day[day] for day in range(1, 8)]          
                # Get the total rule count in the current week
                total_rules_in_week = Rule.objects.filter(created_at__gte=start_of_week).count()
                
                # Obtener los tipos de sistemas de detección únicos
                detection_system_types = DetectionSystem.objects.values_list('type', flat=True).distinct()

                # Realizar la búsqueda de reglas por tipo de sistema de detección y contar el número de reglas para cada tipo
                rule_counts_by_detection_system = Rule.objects.values('detection_systems__type').annotate(rule_count=Count('id'))

                # Crear un diccionario para almacenar los conteos de reglas por tipo de sistema de detección
                total_rules_by_detection_system_type = {system_type: 0 for system_type in detection_system_types}

                # Actualizar el diccionario con los conteos reales
                for entry in rule_counts_by_detection_system:
                    system_type = entry['detection_systems__type']
                    rule_count = entry['rule_count']
                    total_rules_by_detection_system_type[system_type] = rule_count
            except:
                rules_by_day_list = [0, 0, 0, 0, 0, 0, 0]
                total_rules_in_week = 0
                pass

            try:
                # Obtener el número de reglas por mes
                rules_by_month = Rule.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

                # Crear un diccionario para almacenar el recuento de reglas por mes
                rules_count_by_month = {month: 0 for month in range(1, 13)}

                # Actualizar el diccionario con los valores reales
                for rule in rules_by_month:
                    month = rule['month']
                    count = rule['count']
                    rules_count_by_month[month] = count

                # Crear una lista con los valores de reglas por mes en orden
                rules_by_month_list = [rules_count_by_month[month] for month in range(1, 13)]
                # Get the total rule count in the year
                total_rules_in_year = Rule.objects.count()
            except:
                total_rules_in_year = 0
                rules_by_month_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                pass

            # Last 6 actions performed by user
            try:
                recent_actions = LogEntry.objects.select_related('user').order_by('-action_time')[:6]
            except:
                pass
            
            # Add the results to the context            
            context.update({
                'total_customers': total_customers,
                'total_users': total_users,
                'total_detection_systems': total_detection_systems,
                'total_rules': total_rules,
                'total_watchers': total_watchers,
                'total_reports': total_reports,
                'top_users_last_day': top_users_last_day,
                'top_users_last_week': top_users_last_week,
                'top_users_last_month': top_users_last_month,
                'rules_by_day_list': rules_by_day_list,
                'total_rules_by_detection_system_type':total_rules_by_detection_system_type,
                'total_rules_in_week': total_rules_in_week,
                'rules_by_month_list': rules_by_month_list,
                'total_rules_in_year': total_rules_in_year,
                'recent_actions': recent_actions,
            })

        
        if load_template == 'tables-customers.html':
            customers = Customer.objects.all()
            
            context['customers'] = customers
        
        if load_template == 'tables-detection_systems.html':
            detection_systems = DetectionSystem.objects.all()
            
            context['detection_systems'] = detection_systems
        
        if load_template == 'tables-rules.html':
            rules = Rule.objects.all()
            
            context['rules'] = rules
            
        if load_template == 'tables-watchers.html':
            watchers = Watcher.objects.all()
            
            context['watchers'] = watchers
        
        if load_template == 'tables-reports.html':
            reports = Report.objects.all()
            
            context['reports'] = reports
            
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
            
            elif object_to_export == 'watchers':
                watchers = Watcher.objects.all()
                response = HttpResponse(
                    content_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="watchers.csv"'},
                )

                writer = csv.writer(response)
                # CSV columns
                writer.writerow(['ID', 'Name', 'Customers', ' Detection Systems', 'Created by', 'Created at (UTC)','Modified at (UTC)'])
                for watcher in watchers:
                    customers = ', '.join([customer.name for customer in watcher.customers.all()])
                    detection_systems = ', '.join([detection_system.name for detection_system in watcher.detection_systems.all()])
                    writer.writerow([watcher.id, watcher.name, customers, detection_systems, watcher.created_by, watcher.created_at, watcher.modified_at])
                # Return the response
                return response
            
            elif object_to_export == 'reports':
                reports = Report.objects.all()
                response = HttpResponse(
                    content_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="reports.csv"'},
                )

                writer = csv.writer(response)
                # CSV columns
                writer.writerow(['ID', 'Name', 'Customers', ' Detection Systems', 'Created by', 'Created at (UTC)','Modified at (UTC)'])
                for report in reports:
                    customers = ', '.join([customer.name for customer in report.customers.all()])
                    detection_systems = ', '.join([detection_system.name for detection_system in report.detection_systems.all()])
                    writer.writerow([report.id, report.name, customers, detection_systems, report.created_by, report.created_at, report.modified_at])
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
    
