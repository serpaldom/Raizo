import datetime
from django.db.models import Count, Avg, Q
from django.contrib.admin.models import LogEntry
from .models import Customer, DetectionSystem, Rule, Watcher, Report, MitreTactic, MitreTechnique
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.admin.models import LogEntry
from django.db.models.functions import ExtractMonth, TruncMonth, TruncDay
from django.utils import timezone
from django.contrib.sessions.models import Session
from .DatabaseManager import DatabaseManager
import csv
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

class DatabaseManager:
    import csv
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
    def export_reports():
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
    