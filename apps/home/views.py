# -*- encoding: utf-8 -*-


from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from .DatabaseManager import DatabaseManager
from .ExportManager import ExportManager
from django.contrib import messages
from django.views.decorators.cache import cache_page
from .models import MitreTactic, Technologies
import csv
import os
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
            # Retrieve various counts from the database
            try:
                total_customers = db_manager.get_total_customers()
                total_users = db_manager.get_total_users()
                total_detection_systems = db_manager.get_total_detection_systems()
                total_rules = db_manager.get_total_rules()
                total_watchers = db_manager.get_total_watchers()
                total_reports = db_manager.get_total_reports()
            except:
                # Set counts to 0 in case of an error
                total_customers = 0
                total_users = 0
                total_detection_systems = 0
                total_rules = 0
                total_watchers = 0
                total_reports = 0
            
            try:
                # Retrieve the top 5 users who created the most rules in the last day
                top_users_rules_last_day = db_manager.get_top_users_rules_last_day(limit=5)

                # Retrieve the top 5 users who created the most rules in the last week
                top_users_rules_last_week = db_manager.get_top_users_rules_last_week(limit=5)

                # Retrieve the top 5 users who created the most rules in the last month
                top_users_rules_last_month = db_manager.get_top_users_rules_last_month(limit=5)

                # Retrieve the top 5 users who created the most watchers in the last day
                top_users_watchers_last_day = db_manager.get_top_users_watchers_last_day(limit=5)

                # Retrieve the top 5 users who created the most watchers in the last week
                top_users_watchers_last_week = db_manager.get_top_users_watchers_last_week(limit=5)

                # Retrieve the top 5 users who created the most watchers in the last month
                top_users_watchers_last_month = db_manager.get_top_users_watchers_last_month(limit=5)

                # Retrieve the top 5 users who created the most reports in the last day
                top_users_reports_last_day = db_manager.get_top_users_reports_last_day(limit=5)

                # Retrieve the top 5 users who created the most reports in the last week
                top_users_reports_last_week = db_manager.get_top_users_reports_last_week(limit=5)

                # Retrieve the top 5 users who created the most reports in the last month
                top_users_reports_last_month = db_manager.get_top_users_reports_last_month(limit=5)
            except Exception as e:
                print(e)
                # Set counts to 0 in case of an error
                top_users_rules_last_day = 0
                top_users_rules_last_week = 0
                top_users_rules_last_month = 0
                top_users_watchers_last_day = 0
                top_users_watchers_last_week = 0
                top_users_watchers_last_month = 0
                top_users_reports_last_day = 0
                top_users_reports_last_week = 0
                top_users_reports_last_month = 0

            try:
                # Retrieve the number of rules by day of the current week
                rules_by_day_of_week = db_manager.get_rules_by_day_of_week()

                # Create a dictionary to store the rule counts by day
                rules_count_by_day = {day: 0 for day in range(1, 8)}

                # Update the dictionary with the actual values
                for rule in rules_by_day_of_week:
                    day = rule['created_at__week_day']
                    count = rule['count']
                    rules_count_by_day[day] = count

                # Create a list with the rule counts by day in order
                rules_by_day_list = [rules_count_by_day[day] for day in range(1, 8)]

                # Get the total rule count in the current week
                total_rules_in_week = db_manager.get_total_rules_in_week()
                
                # Perform a search for rule counts by detection system type and count the number of rules for each type
                rule_counts_by_detection_system = db_manager.get_rule_counts_by_detection_system()

                # Retrieve the number of reports by day of the current week
                reports_by_day_of_week = db_manager.get_reports_by_day_of_week()

                # Create a dictionary to store the report counts by day
                reports_count_by_day = {day: 0 for day in range(1, 8)}

                # Update the dictionary with the actual values
                for report in reports_by_day_of_week:
                    day = report['created_at__week_day']
                    count = report['count']
                    reports_count_by_day[day] = count

                # Create a list with the report counts by day in order
                reports_by_day_list = [reports_count_by_day[day] for day in range(1, 8)]

                # Retrieve the number of watchers by day of the current week
                watchers_by_day_of_week = db_manager.get_watchers_by_day_of_week()

                # Create a dictionary to store the watcher counts by day
                watchers_count_by_day = {day: 0 for day in range(1, 8)}

                # Update the dictionary with the actual values
                for watcher in watchers_by_day_of_week:
                    day = watcher['created_at__week_day']
                    count = watcher['count']
                    watchers_count_by_day[day] = count

                # Create a list with the watcher counts by day in order
                watchers_by_day_list = [watchers_count_by_day[day] for day in range(1, 8)]

                # Get the total watcher count in the current week
                total_watchers_in_week = db_manager.get_total_watchers_in_week()
                
                # Get the total reports count in the current week
                total_reports_in_week = db_manager.get_total_reports_in_week()

                # Retrieve the number of rules by month
                rules_by_month = db_manager.get_rules_by_month()

                # Create a dictionary to store the rule counts by month
                rules_count_by_month = {month: 0 for month in range(1, 13)}

                # Update the dictionary with the actual values
                for rule in rules_by_month:
                    month = rule['month']
                    count = rule['count']
                    rules_count_by_month[month] = count

                # Create a list with the rule counts by month in order
                rules_by_month_list = [rules_count_by_month[month] for month in range(1, 13)]

                # Get the total rule count in the year
                total_rules_in_year = db_manager.get_total_rules_in_year()

                # Retrieve the number of reports by month
                reports_by_month = db_manager.get_reports_by_month()

                # Create a dictionary to store the report counts by month
                reports_count_by_month = {month: 0 for month in range(1, 13)}

                # Update the dictionary with the actual values
                for report in reports_by_month:
                    month = report['month']
                    count = report['count']
                    reports_count_by_month[month] = count

                # Create a list with the report counts by month in order
                reports_by_month_list = [reports_count_by_month[month] for month in range(1, 13)]

                # Retrieve the number of watchers by month
                watchers_by_month = db_manager.get_watchers_by_month()

                # Create a dictionary to store the watcher counts by month
                watchers_count_by_month = {month: 0 for month in range(1, 13)}

                # Update the dictionary with the actual values
                for watcher in watchers_by_month:
                    month = watcher['month']
                    count = watcher['count']
                    watchers_count_by_month[month] = count

                # Create a list with the watcher counts by month in order
                watchers_by_month_list = [watchers_count_by_month[month] for month in range(1, 13)]

                # Get the total watcher count in the year
                total_watchers_in_year = db_manager.get_total_watchers_in_year()
                
                # Get the total reports count in the year
                total_reports_in_year = db_manager.get_total_reports_in_year()

            except:
                # Set counts and lists to 0 in case of an error
                rules_by_day_list = [0, 0, 0, 0, 0, 0, 0]
                total_rules_in_week = 0
                reports_by_day_list = [0, 0, 0, 0, 0, 0, 0]
                total_reports_in_week = 0
                watchers_by_day_list = [0, 0, 0, 0, 0, 0, 0]
                total_watchers_in_week = 0
                rules_by_month_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_rules_in_year = 0
                reports_by_month_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_reports_in_year = 0
                watchers_by_month_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                total_watchers_in_year = 0
                pass


            try:
                # Retrieve the number of rules by month
                rules_by_month = db_manager.get_rules_by_month()

                # Create a dictionary to store the rule counts by month
                rules_count_by_month = {month: 0 for month in range(1, 13)}

                # Update the dictionary with the actual values
                for rule in rules_by_month:
                    month = rule['month']
                    count = rule['count']
                    rules_count_by_month[month] = count

                # Create a list with the rule counts by month in order
                rules_by_month_list = [rules_count_by_month[month] for month in range(1, 13)]

                # Get the total rule count in the year
                total_rules_in_year = db_manager.get_total_rules_in_year()
            except:
                # Set counts and lists to 0 in case of an error
                total_rules_in_year = 0
                rules_by_month_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                pass
            
            # Rule - Tactic Mitre distribution
            try:
                tactic_ids = db_manager.get_tactic_ids()
                distribution_by_tactic = db_manager.get_distribution_by_tactic()
                distribution_by_tactic_list = [next((tactic['count'] for tactic in distribution_by_tactic if tactic['mitre_tactics__id'] == tactic_id), 0) for tactic_id in tactic_ids]
            except:
                # Set counts to 0 in case of an error
                distribution_by_tactic = 0
                pass
            
            # Rule - Severity distribution
            severity_order = ['Critical', 'Very High', 'High', 'Medium', 'Low', 'Informational']
            distribution_by_severity_list = []
            try:
                distribution_by_severity = db_manager.get_distribution_by_severity()
                
                # Get the rule count for each severity in the specified order
                for severity in severity_order:
                    count = next((item['count'] for item in distribution_by_severity if item['severity'] == severity), 0)
                    distribution_by_severity_list.append(count)
            except:
                # Set counts to 0 in case of an error
                distribution_by_severity_list = [0] * len(severity_order)
                pass
            
            try:
                recent_rules = db_manager.get_recent_rules()
            except:
                # Set recent_rules to an empty string in case of an error
                recent_rules = ""
                pass
            
            try:
                rule_counts_by_technology = db_manager.get_rule_counts_by_technology()
            except Exception as e:
                rule_counts_by_technology = None

            # Last 6 actions performed by user
            try:
                recent_actions = db_manager.get_recent_actions(limit=7)
            except:
                pass
            
            # Current active sessions
            try:
                current_sessions = db_manager.get_current_sessions()
            except:
                # Set current_sessions to 0 in case of an error
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
                
                'top_users_rules_last_day': top_users_rules_last_day,
                'top_users_rules_last_week': top_users_rules_last_week,
                'top_users_rules_last_month': top_users_rules_last_month,
                'top_users_watchers_last_day': top_users_watchers_last_day,
                'top_users_watchers_last_week': top_users_watchers_last_week,
                'top_users_watchers_last_month': top_users_watchers_last_month,
                'top_users_reports_last_day': top_users_reports_last_day,
                'top_users_reports_last_week': top_users_reports_last_week,
                'top_users_reports_last_month': top_users_reports_last_month,
                
                'rules_by_day_list': rules_by_day_list,
                'total_rules_by_detection_system_type': rule_counts_by_detection_system,
                'total_rules_in_week': total_rules_in_week,
                'rules_by_month_list': rules_by_month_list,
                'total_rules_in_year': total_rules_in_year,
                
                'watchers_by_day_list': watchers_by_day_list,
                'total_watchers_in_week': total_watchers_in_week,
                'watchers_by_month_list': watchers_by_month_list,
                'total_watchers_in_year': total_watchers_in_year,
                
                'reports_by_day_list': reports_by_day_list,
                'total_reports_in_week': total_reports_in_week,
                'reports_by_month_list': reports_by_month_list,
                'total_reports_in_year': total_reports_in_year,
                
                'distribution_by_tactic': distribution_by_tactic_list,
                'distribution_by_severity': distribution_by_severity_list,
                
                'recent_rules': recent_rules,
                'rule_counts_by_technology':rule_counts_by_technology,
                'recent_actions': recent_actions,
                'current_sessions': current_sessions,
            })


        
        if load_template == 'tables-customers.html':
            # Retrieve all customers from the database
            customers = db_manager.get_all_customers()
            context['customers'] = customers

        if load_template == 'tables-detection_systems.html':
            # Retrieve all detection systems from the database
            detection_systems = db_manager.get_all_detection_systems()
            context['detection_systems'] = detection_systems

        if load_template == 'tables-rules.html':
            # Retrieve all rules from the database
            rules = db_manager.get_all_rules()
            context['rules'] = rules

        if load_template == 'tables-watchers.html':
            # Retrieve all watchers from the database
            watchers = db_manager.get_all_watchers()
            context['watchers'] = watchers

        if load_template == 'tables-reports.html':
            # Retrieve all reports from the database
            reports = db_manager.get_all_reports()
            context['reports'] = reports

        if load_template == 'profile.html':
            try:
                # Retrieve user-specific data for the profile page
                context['user_rules'] = db_manager.get_user_rules(request.user)
                context['user_watchers'] = db_manager.get_user_watchers(request.user)
                context['user_reports'] = db_manager.get_user_reports(request.user)
                
                # Check if the user is in the top users of the last week
                context['user_in_top_last_week'] = request.user in db_manager.get_top_users_rules_last_week(limit=5)
                
                # Check if the user is in the top users of the last month
                context['user_in_top_last_month'] = request.user in db_manager.get_top_users_rules_last_month(limit=5)
            except:
                # Set user-specific data to empty strings in case of an error
                context['user_rules'] = ""
                context['user_watchers'] = ""
                context['user_reports'] = ""
                context['user_in_top_last_week'] = ""
                context['user_in_top_last_month'] = ""
                context['detection_systems'] = ""
                pass

        if load_template == 'edit-profile.html':
            if request.method == 'POST':
                # Get the fields sent in the POST request
                theme_preferences ={
                    "Light": "light",
                    "Dark": "dark"
                }
                theme_preference = request.POST.get('theme_preference')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')

                # Check if the password fields match
                if password != confirm_password:
                    messages.error(request, 'Passwords do not match.')
                    return redirect('edit_profile.html')  # Redirect back to the edit form

                # Update the fields in the user object
                user = request.user
                if theme_preferences.get(theme_preference) != user.userpreferences.theme_preference:
                    user.userpreferences.theme_preference = theme_preferences.get(theme_preference)
                    user.userpreferences.save()
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
                return redirect('profile.html')  # Redirect to the profile page or wherever you desire

        if request.path.split('/')[1] == 'export':
            object_to_export = request.path.split('/')[-1]
            if object_to_export == 'customers':
               return export_manager.export_customers()

            elif object_to_export == 'detection_systems':
                return export_manager.export_detection_systems()
            
            elif object_to_export == 'rules':
                return export_manager.export_rules()

            elif object_to_export == 'watchers':
                return export_manager.export_watchers()

            elif object_to_export == 'reports':
                return export_manager.export_reports()

            elif object_to_export == 'dashboard':
                print("TODO")


        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        # Handle the case when the template does not exist
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        # Handle any other exceptions
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
