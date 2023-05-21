# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from .models import Customer, DetectionSystem, Rule, Watcher, Report, MitreTactic, MitreTechnique, Technologies, Tag
from django.contrib.auth.models import User
import csv
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta, date
from django.contrib.admin.models import LogEntry
from django.db.models.functions import ExtractMonth
from .DatabaseManager import DatabaseManager
from .ExportManager import ExportManager
from django.template.loader import render_to_string

db_manager  = DatabaseManager()
export_manager = ExportManager()

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
            
            try:
                total_customers = db_manager.get_total_customers()
                total_users = db_manager.get_total_users()
                total_detection_systems = db_manager.get_total_detection_systems()
                total_rules = db_manager.get_total_rules()
                total_watchers = db_manager.get_total_watchers()
                total_reports = db_manager.get_total_reports()
            except:
                total_customers = 0
                total_users = 0
                total_detection_systems = 0
                total_rules = 0
                total_watchers = 0
                total_reports = 0
            
            try:
                # Obtener los 3 usuarios que han creado la mayor cantidad de Rule en el último día
                top_users_last_day = db_manager.get_top_users_last_day(limit=5)

                # Obtener los 3 usuarios que han creado la mayor cantidad de Rule en los últimos 7 días
                top_users_last_week = db_manager.get_top_users_last_week(limit=5)

                # Obtener los 3 usuarios que han creado la mayor cantidad de Rule en el último mes
                top_users_last_month = db_manager.get_top_users_last_month(limit=5)
            except:
                top_users_last_day = 0
                top_users_last_week = 0
                top_users_last_month = 0

            try:
                # Obtener el número de reglas por día de la semana actual
                rules_by_day_of_week = db_manager.get_rules_by_day_of_week()

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
                total_rules_in_week = db_manager.get_total_rules_in_week()
                
                # Obtener los tipos de sistemas de detección únicos
                detection_system_types = db_manager.get_detection_system_types()

                # Realizar la búsqueda de reglas por tipo de sistema de detección y contar el número de reglas para cada tipo
                rule_counts_by_detection_system = db_manager.get_rule_counts_by_detection_system()

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
                total_rules_by_detection_system_type = []
                pass

            try:
                # Obtener el número de reglas por mes
                rules_by_month = db_manager.get_rules_by_month()

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
                total_rules_in_year = db_manager.get_total_rules_in_year()
            except:
                total_rules_in_year = 0
                rules_by_month_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                pass
            
            # Rule - Tactic Mitre distribution
            try:
                tactic_ids = db_manager.get_tactic_ids()
                distribution_by_tactic = db_manager.get_distribution_by_tactic()
                distribution_by_tactic_list = [next((tactic['count'] for tactic in distribution_by_tactic if tactic['mitre_tactics__id'] == tactic_id), 0) for tactic_id in tactic_ids]
            except:
                distribution_by_tactic = 0
                pass
            
            # Rule - Severity distribution
            severity_order = ['Critical', 'Very High', 'High', 'Medium', 'Low', 'Informational']
            distribution_by_severity_list = []
            try:
                distribution_by_severity = db_manager.get_distribution_by_severity()
                
                # Obtener el recuento de reglas para cada severidad en el orden especificado
                for severity in severity_order:
                    count = next((item['count'] for item in distribution_by_severity if item['severity'] == severity), 0)
                    distribution_by_severity_list.append(count)       
            except:
                # En caso de que ocurra una excepción, establecer todos los recuentos en 0
                distribution_by_severity_list = [0] * len(severity_order)
                pass
            
            try:
                recent_rules = db_manager.get_recent_rules()  
            except:
                # En caso de que ocurra una excepción, establecer todos los recuentos en 0
                recent_rules = ""
                pass

            # Last 6 actions performed by user
            try:
                recent_actions = db_manager.get_recent_actions(limit=7)
            except:
                pass
            
            # Current active sessions
            try:
                current_sessions = db_manager.get_current_sessions()
            except:
                current_sessions = 0
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
                'distribution_by_tactic':distribution_by_tactic_list,
                'distribution_by_severity':distribution_by_severity_list,
                'recent_rules': recent_rules,
                'recent_actions': recent_actions,
                'current_sessions': current_sessions,
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
            
        if load_template == 'profile.html':
            # Get all detection systems for the sidebar
            try:
                detection_systems = db_manager.get_all_detection_systems()
            except:
                detection_systems = 0
                pass
            context['user_rules'] = db_manager.get_user_rules(request.user)
            context['user_watchers'] = db_manager.get_user_watchers(request.user)
            context['user_reports'] = db_manager.get_user_reports(request.user)
            context['user_in_top_last_week'] = request.user in db_manager.get_top_users_last_week(limit=5)
            context['user_in_top_last_month'] = request.user in db_manager.get_top_users_last_week(limit=5)
            context['detection_systems'] = detection_systems
            
        if request.path.split('/')[1] == 'export':
            object_to_export = request.path.split('/')[-1]
            if object_to_export == 'customers':
                export_manager.export_customers()
            
            elif object_to_export == 'detection_systems':
                export_manager.export_detection_systems()
            
            elif object_to_export == 'watchers':
                export_manager.export_watchers()
            
            elif object_to_export == 'reports':
                export_manager.export_reports()
            
            elif object_to_export == 'dashboard':
                
                print("TODO")
            
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    