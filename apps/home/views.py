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
from django.contrib import messages

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
    '''
    # Código para crear el diccionario de técnicas de MITRE
    mitre_techniques_data = {
        'T1548': 'Abuse Elevation Control Mechanism',
        'T1548.001': 'Abuse Elevation Control Mechanism: Setuid and Setgid',
        'T1548.002': 'Abuse Elevation Control Mechanism: Bypass User Account Control',
        'T1548.003': 'Abuse Elevation Control Mechanism: Sudo and Sudo Caching',
        'T1548.004': 'Abuse Elevation Control Mechanism: Elevated Execution with Prompt',
        'T1134': 'Access Token Manipulation',
        'T1134.001': 'Access Token Manipulation: Token Impersonation/Theft',
        'T1134.002': 'Access Token Manipulation: Create Process with Token',
        'T1134.003': 'Access Token Manipulation: Make and Impersonate Token',
        'T1134.004': 'Access Token Manipulation: Parent PID Spoofing',
        'T1134.005': 'Access Token Manipulation: SID-History Injection',
        'T1547': 'Boot or Logon Autostart Execution',
        'T1547.001': 'Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder',
        'T1547.002': 'Boot or Logon Autostart Execution: Authentication Package',
        'T1547.003': 'Boot or Logon Autostart Execution: Time Providers',
        'T1547.004': 'Boot or Logon Autostart Execution: Winlogon Helper DLL',
        'T1547.005': 'Boot or Logon Autostart Execution: Security Support Provider',
        'T1547.006': 'Boot or Logon Autostart Execution: Kernel Modules and Extensions',
        'T1547.007': 'Boot or Logon Autostart Execution: Re-opened Applications',
        'T1547.008': 'Boot or Logon Autostart Execution: LSASS Driver',
        'T1547.009': 'Boot or Logon Autostart Execution: Shortcut Modification',
        'T1547.010': 'Boot or Logon Autostart Execution: Port Monitors',
        'T1547.012': 'Boot or Logon Autostart Execution: Print Processors',
        'T1547.013': 'Boot or Logon Autostart Execution: XDG Autostart Entries',
        'T1547.014': 'Boot or Logon Autostart Execution: Active Setup',
        'T1547.015': 'Boot or Logon Autostart Execution: Login Items',
        'T1037': 'Boot or Logon Initialization Scripts',
        'T1037.001': 'Boot or Logon Initialization Scripts: Logon Script (Windows)',
        'T1037.002': 'Boot or Logon Initialization Scripts: Login Hook',
        'T1037.003': 'Boot or Logon Initialization Scripts: Network Logon Script',
        'T1037.004': 'Boot or Logon Initialization Scripts: RC Scripts',
        'T1037.005': 'Boot or Logon Initialization Scripts: Startup Items',
        'T1543': 'Create or Modify System Process',
        'T1543.001': 'Create or Modify System Process: Launch Agent',
        'T1543.002': 'Create or Modify System Process: Systemd Service',
        'T1543.003': 'Create or Modify System Process: Windows Service',
        'T1543.004': 'Create or Modify System Process: Launch Daemon',
        'T1484': 'Domain Policy Modification',
        'T1484.001': 'Domain Policy Modification: Group Policy Modification',
        'T1484.002': 'Domain Policy Modification: Domain Trust Modification',
        'T1611': 'Escape to Host',
        'T1546': 'Event Triggered Execution',
        'T1546.001': 'Event Triggered Execution: Change Default File Association',
        'T1546.002': 'Event Triggered Execution: Screensaver',
        'T1546.003': 'Event Triggered Execution: Windows Management Instrumentation Event Subscription',
        'T1546.004': 'Event Triggered Execution: Unix Shell Configuration Modification',
        'T1546.005': 'Event Triggered Execution: Trap',
        'T1546.006': 'Event Triggered Execution: LC_LOAD_DYLIB Addition',
        'T1546.007': 'Event Triggered Execution: Netsh Helper DLL',
        'T1546.008': 'Event Triggered Execution: Accessibility Features',
        'T1546.009': 'Event Triggered Execution: AppCert DLLs',
        'T1546.010': 'Event Triggered Execution: AppInit DLLs',
        'T1546.011': 'Event Triggered Execution: Application Shimming',
        'T1546.012': 'Event Triggered Execution: Image File Execution Options Injection',
        'T1546.013': 'Event Triggered Execution: PowerShell Profile',
        'T1546.014': 'Event Triggered Execution: Emond',
        'T1546.015': 'Event Triggered Execution: Component Object Model Hijacking',
        'T1546.016': 'Event Triggered Execution: Installer Packages',
        'T1068': 'Exploitation for Privilege Escalation',
        'T1574': 'Hijack Execution Flow',
        'T1574.001': 'Hijack Execution Flow: DLL Search Order Hijacking',
        'T1574.002': 'Hijack Execution Flow: DLL Side-Loading',
        'T1574.004': 'Hijack Execution Flow: Dylib Hijacking',
        'T1574.005': 'Hijack Execution Flow: Executable Installer File Permissions Weakness',
        'T1574.006': 'Hijack Execution Flow: Dynamic Linker Hijacking',
        'T1574.007': 'Hijack Execution Flow: Path Interception by PATH Environment Variable',
        'T1574.008': 'Hijack Execution Flow: Path Interception by Search Order Hijacking',
        'T1574.009': 'Hijack Execution Flow: Path Interception by Unquoted Path',
        'T1574.010': 'Hijack Execution Flow: Services File Permissions Weakness',
        'T1574.011': 'Hijack Execution Flow: Services Registry Permissions Weakness',
        'T1574.012': 'Hijack Execution Flow: COR_PROFILER',
        'T1574.013': 'Hijack Execution Flow: KernelCallbackTable',
        'T1055': 'Process Injection',
        'T1055.001': 'Process Injection: Dynamic-link Library Injection',
        'T1055.002': 'Process Injection: Portable Executable Injection',
        'T1055.003': 'Process Injection: Thread Execution Hijacking',
        'T1055.004': 'Process Injection: Asynchronous Procedure Call',
        'T1055.005': 'Process Injection: Thread Local Storage',
        'T1055.008': 'Process Injection: Ptrace System Calls',
        'T1055.009': 'Process Injection: Proc Memory',
        'T1055.011': 'Process Injection: Extra Window Memory Injection',
        'T1055.012': 'Process Injection: Process Hollowing',
        'T1055.013': 'Process Injection: Process Doppelgänging',
        'T1055.014': 'Process Injection: VDSO Hijacking',
        'T1055.015': 'Process Injection: ListPlanting',
        'T1053': 'Scheduled Task/Job',
        'T1053.002': 'Scheduled Task/Job: At',
        'T1053.003': 'Scheduled Task/Job: Cron',
        'T1053.005': 'Scheduled Task/Job: Scheduled Task',
        'T1053.006': 'Scheduled Task/Job: Systemd Timers',
        'T1053.007': 'Scheduled Task/Job: Container Orchestration Job',
        'T1078.001': 'Valid Accounts: Default Accounts',
        'T1078.002': 'Valid Accounts: Domain Accounts',
        'T1078.003': 'Valid Accounts: Local Accounts',
        'T1078.004': 'Valid Accounts: Cloud Accounts'
    }


    mitre_tactic_id = 'TA0004'  # ID de la táctica
    mitre_tactic_name = 'Privilege Escalation'  # Nombre de la táctica
    # Crear las técnicas de MITRE asociadas a la táctica "Persistence" con el ID "TA0003"
    mitre_tactic = MitreTactic.objects.get(id=mitre_tactic_id, name=mitre_tactic_name)

    for technique_id, technique_name in mitre_techniques_data.items():
        mitre_technique, created = MitreTechnique.objects.get_or_create(
            id=technique_id,
            name=technique_name
        )
        if not created:  # Verificar si la técnica ya existe
            mitre_technique.mitre_tactics.add(mitre_tactic)  # Añadir la táctica existente
        else:
            mitre_technique.save()  # Guardar la técnica creada'''

    
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

                # Realizar la búsqueda de reglas por tipo de sistema de detección y contar el número de reglas para cada tipo
                rule_counts_by_detection_system = db_manager.get_rule_counts_by_detection_system()
                
            except:
                rules_by_day_list = [0, 0, 0, 0, 0, 0, 0]
                total_rules_in_week = 0
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
                'total_rules_by_detection_system_type':rule_counts_by_detection_system,
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
            try:
                context['user_rules'] = db_manager.get_user_rules(request.user)
                context['user_watchers'] = db_manager.get_user_watchers(request.user)
                context['user_reports'] = db_manager.get_user_reports(request.user)
                context['user_in_top_last_week'] = request.user in db_manager.get_top_users_last_week(limit=5)
                context['user_in_top_last_month'] = request.user in db_manager.get_top_users_last_month(limit=5)
            except:
                context['user_rules'] = ""
                context['user_watchers'] = ""
                context['user_reports'] = ""
                context['user_in_top_last_week'] = ""
                context['user_in_top_last_month'] = ""
                context['detection_systems'] = ""
                pass
            
        if load_template == 'edit-profile.html':
            if request.method == 'POST':
                # Obtener los campos enviados en la solicitud POST
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')

                # Verificar si los campos de contraseña coinciden
                if password != confirm_password:
                    messages.error(request, 'Passwords do not match.')
                    return redirect('edit_profile.html')  # Redirigir nuevamente al formulario de edición

                # Actualizar los campos en el objeto de usuario
                user = request.user
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                if email:
                    user.email = email
                if password:
                    user.set_password(password)
                user.save()
                
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile.html')  # Redirigir a la página de perfil o a donde desees
            
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
    