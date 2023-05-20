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

class DatabaseManager:
    def __init__(self):
        self.now = timezone.now()
        self.last_day = self.now - timezone.timedelta(days=1)
        self.last_week = self.now - timezone.timedelta(days=7)
        self.last_month = self.now - timezone.timedelta(days=30)
        self.today = timezone.localdate()
        self.start_of_week = self.today - timezone.timedelta(days=self.today.weekday())
        self.end_of_week = self.start_of_week + timezone.timedelta(days=6)
   
    def get_total_customers(self):
        """
        Get the total number of customers.
        """
        return Customer.objects.count()

    def get_total_users(self):
        """
        Get the total number of users.
        """
        return User.objects.count()

    def get_total_detection_systems(self):
        """
        Get the total number of detection systems.
        """
        return DetectionSystem.objects.count()

    def get_total_rules(self):
        """
        Get the total number of rules.
        """
        return Rule.objects.count()

    def get_total_watchers(self):
        """
        Get the total number of watchers.
        """
        return Watcher.objects.count()

    def get_total_reports(self):
        """
        Get the total number of reports.
        """
        return Report.objects.count()

    def get_top_users_last_day(self, limit=3):
        """
        Get the top users who created the most rules in the last day.
        """
        return User.objects.annotate(total_rules=Count('created_rules')).filter(
            created_rules__created_at__gte=self.last_day
        ).order_by('-total_rules')[:limit]

    def get_top_users_last_week(self, limit=3):
        """
        Get the top users who created the most rules in the last week.
        """
        return User.objects.annotate(total_rules=Count('created_rules')).filter(
            created_rules__created_at__gte=self.last_week
        ).order_by('-total_rules')[:limit]

    def get_top_users_last_month(self, limit=3):
        """
        Get the top users who created the most rules in the last month.
        """
        return User.objects.annotate(total_rules=Count('created_rules')).filter(
            created_rules__created_at__gte=self.last_month
        ).order_by('-total_rules')[:limit]

    def get_rules_by_day_of_week(self):
        """
        Get the number of rules created per day of the week.
        """
        return Rule.objects.filter(created_at__gte=self.start_of_week).values('created_at__week_day').annotate(
            count=Count('id')
        ).order_by('created_at__week_day')

    def get_total_rules_in_week(self):
        """
        Get the total number of rules created in the current week.
        """
        return Rule.objects.filter(created_at__gte=self.start_of_week).count()

    def get_detection_system_types(self):
        """
        Get unique detection system types.
        """
        return DetectionSystem.objects.values_list('type', flat=True).distinct()

    def get_rule_counts_by_detection_system(self):
        """
        Get the count of rules per detection system.
        """
        return Rule.objects.values('detection_systems__type').annotate(rule_count=Count('id'))

    def get_rules_by_month(self):
        """
        Get the number of rules created per month.
        """
        return Rule.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(
            count=Count('id')
        ).order_by('month')

    def get_total_rules_in_year(self):
        """
        Get the total number of rules created in the current year.
        """
        return Rule.objects.count()
    
    def get_tactic_ids(self):
        """
        Get the tactic IDs ordered by ID.
        """
        return MitreTactic.objects.values_list('id', flat=True).order_by('id')

    def get_distribution_by_tactic(self):
        """
        Get the distribution of rules by MITRE tactic.
        """
        return Rule.objects.values('mitre_tactics__id').annotate(count=Count('id')).order_by('mitre_tactics__id')

    def get_recent_actions(self, limit=6):
        """
        Get the recent log actions.
        """
        return LogEntry.objects.select_related('user').order_by('-action_time')[:limit]

    def get_rule_counts_by_user(self):
        """
        Get the count of rules created by each user.
        """
        return User.objects.values('username').annotate(rule_count=Count('created_rules'))

    def get_rule_counts_by_detection_type(self):
        """
        Get the count of rules created for each detection type.
        """
        return Rule.objects.values('detection_systems__type').annotate(rule_count=Count('id'))

    def get_average_rules_per_user(self):
        """
        Get the average number of rules created per user.
        """
        return User.objects.annotate(rule_count=Count('created_rules')).aggregate(average=Avg('rule_count'))

    def get_user_with_most_rules(self):
        """
        Get the user with the highest number of created rules.
        """
        return User.objects.annotate(rule_count=Count('created_rules')).order_by('-rule_count').first()

    def get_rules_within_date_range(self, start_date, end_date):
        """
        Get the rules created within a specific date range.
        """
        return Rule.objects.filter(created_at__range=[start_date, end_date])

    def get_rules_by_detection_system(self, system_id):
        """
        Get the rules created for a specific detection system.
        """
        return Rule.objects.filter(detection_systems__id=system_id)

    def get_rules_by_user(self, user_id):
        """
        Get the rules created by a specific user.
        """
        return Rule.objects.filter(created_by__id=user_id)

    def get_rule_counts_by_month(self):
        """
        Get the count of rules created for each month.
        """
        return Rule.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')

    def get_rule_counts_by_day(self):
        """
        Get the count of rules created for each day.
        """
        return Rule.objects.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by('day')

    def get_recent_rules(self, limit=10):
        """
        Get the most recent rules.
        """
        return Rule.objects.order_by('-created_at')[:limit]

    def get_rules_by_tag(self, tag):
        """
        Get the rules related to a specific tag.
        """
        return Rule.objects.filter(tags__name=tag)
    
    def search_rules(self, query):
        """
        Search for rules that match a given query.
        """
        return Rule.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    def get_rules_by_mitre_tactic(self, tactic_id):
        """
        Get all rules associated with a specific MITRE tactic.
        """
        return Rule.objects.filter(mitre_tactics__id=tactic_id)

    def get_rules_by_mitre_technique(self, technique_id):
        """
        Get all rules associated with a specific MITRE technique.
        """
        return Rule.objects.filter(mitre_techniques__id=technique_id)

    def get_rules_by_severity(self):
            """
            Get the number of rules grouped by severity.
            """
            return Rule.objects.values('severity').annotate(count=Count('id')).order_by('severity')

    def get_top_rules_by_severity(self, severity, limit=3):
        """
        Get the top rules by severity.
        """
        return Rule.objects.filter(severity=severity).order_by('-created_at')[:limit]
    
    def get_distribution_by_severity(self):
        """
        Get the distribution of rules by severity.
        """
        return Rule.objects.values('severity').annotate(count=Count('id')).order_by('severity')
    
    def get_current_sessions(self):
        """
        Get the current active sessions in the app.
        """
        return Session.objects.filter(expire_date__gte=timezone.now())