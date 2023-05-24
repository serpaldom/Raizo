from .models import Customer, DetectionSystem, Watcher, Report, Rule
import csv
from django.http import HttpResponse
from django.http import HttpResponse

class ExportManager:
    
    @staticmethod
    def export_customers():
        customers = Customer.objects.all()
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="customers.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Initials', 'Detection systems', 'Created by', 'Created at (UTC)', 'Modified at (UTC)'])
        for customer in customers:
            detection_systems = ', '.join([ds.name for ds in customer.detection_systems.all()])
            writer.writerow([customer.id, customer.name, customer.initials, detection_systems, customer.created_by, customer.created_at, customer.modified_at])

        return response

    @staticmethod
    def export_detection_systems():
        detection_systems = DetectionSystem.objects.all()
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="detection_systems.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Type', 'Customers', 'Created by', 'Created at (UTC)', 'Modified at (UTC)'])
        for detection_system in detection_systems:
            customers = ', '.join([customer.name for customer in detection_system.customers.all()])
            writer.writerow([detection_system.id, detection_system.name, detection_system.type, customers, detection_system.created_by, detection_system.created_at, detection_system.modified_at])

        return response
    
    @staticmethod
    def export_rules():
        rules = Rule.objects.all()
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="rules.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Severity', 'Mitre Tactics', 'Mitre Techniques', 'Technologies', 'Tags', 'Created by', 'Created at (UTC)', 'Modified at (UTC)'])
        for rule in rules:
            mitre_tactics = ', '.join([tactic.name for tactic in rule.mitre_tactics.all()])
            mitre_techniques = ', '.join([technique.name for technique in rule.mitre_techniques.all()])
            technologies = ', '.join([technology.name for technology in rule.technologies.all()])
            tags = ', '.join([tag.name for tag in rule.tags.all()])
            writer.writerow([rule.id, rule.name, rule.severity, mitre_tactics, mitre_techniques, technologies, tags, rule.created_by, rule.created_at, rule.modified_at])

        return response

    
    @staticmethod
    def export_reports():
        reports = Report.objects.all()
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="reports.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Customers', ' Detection Systems', 'Created by', 'Created at (UTC)', 'Modified at (UTC)'])
        for report in reports:
            customers = ', '.join([customer.name for customer in report.customers.all()])
            detection_systems = ', '.join([detection_system.name for detection_system in report.detection_systems.all()])
            writer.writerow([report.id, report.name, customers, detection_systems, report.created_by, report.created_at, report.modified_at])

        return response
    
    @staticmethod
    def export_watchers():
        watchers = Watcher.objects.all()
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="watchers.csv"'},
        )

        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'Customers', ' Detection Systems', 'Created by', 'Created at (UTC)', 'Modified at (UTC)'])
        for watcher in watchers:
            customers = ', '.join([customer.name for customer in watcher.customers.all()])
            detection_systems = ', '.join([detection_system.name for detection_system in watcher.detection_systems.all()])
            writer.writerow([watcher.id, watcher.name, customers, detection_systems, watcher.created_by, watcher.created_at, watcher.modified_at])

        return response
    