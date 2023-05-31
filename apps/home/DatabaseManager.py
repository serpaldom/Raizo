from django.db.models import Count, Avg, Q
from django.contrib.admin.models import LogEntry
from .models import Customer, DetectionSystem, Rule, Watcher, Report, MitreTactic, MitreTechnique, Exceptions
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
        self.current_year = timezone.now().year
        
    def get_all_customers(self):
        """
        Get all customers.
        """
        return Customer.objects.all()

    def get_all_users(self):
        """
        Get all users.
        """
        return User.objects.all()

    def get_all_detection_systems(self):
        """
        Get all detection systems.
        """
        return DetectionSystem.objects.all()

    def get_all_rules(self):
        """
        Get all rules.
        """
        return Rule.objects.all()
    
    def get_all_exceptions(self):
        """
        Get all exceptions.
        """
        return Exceptions.objects.all()

    def get_all_watchers(self):
        """
        Get all watchers.
        """
        return Watcher.objects.all()

    def get_all_reports(self):
        """
        Get all reports.
        """
        return Report.objects.all()
   
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
    
    def get_rule_details(self, rule_id):
        """
        Get all details of a rule and its exceptions.
        """
        try:
            rule = Rule.objects.get(id=rule_id)

            rule_data = {
                'id': rule.id,
                'name': rule.name,
                'severity': rule.severity,
                'mitre_tactics': list(rule.mitre_tactics.values_list('name', flat=True)),
                'mitre_techniques': list(rule.mitre_techniques.values_list('name', flat=True)),
                'technologies': list(rule.technologies.values_list('name', flat=True)),
                'tags': list(rule.tags.values_list('name', flat=True)),
                'detection_systems': list(rule.detection_systems.values_list('name', flat=True)),
                'created_by': rule.created_by.username,
                'created_at': rule.created_at,
            }

            return rule_data
        except Rule.DoesNotExist:
            return None
    def get_exceptions_by_rule_id(self, rule_id):
        """
        Get all exceptions for a specific rule.
        """
        return Exceptions.objects.filter(rule_id=rule_id)

    def get_expired_exceptions_ids(self):
        """
        Retrieve the IDs and expiration dates of exceptions whose expiration time has passed.

        Returns:
            list: A list of dictionaries containing the IDs and expiration dates of expired exceptions.
        """
        # Filter exceptions whose expiration time has passed
        expired_exceptions = Exceptions.objects.filter(Q(expiration_at__lt=self.now), Q(expiration_at__isnull=False))

        # Get the IDs and expiration dates of expired exceptions
        expired_exceptions_data = expired_exceptions.values('id', 'expiration_at')

        # Convert the queryset into a list of dictionaries
        expired_exceptions_list = list(expired_exceptions_data)

        return expired_exceptions_list

    def get_top_users_rules_last_day(self, limit=3):
        """
        Get the top users who created the most rules in the last day.
        """
        return User.objects.annotate(total_rules=Count('rules')).filter(
            rules__created_at__gte=self.last_day
        ).order_by('-total_rules')[:limit]

    def get_top_users_rules_last_week(self, limit=3):
        """
        Get the top users who created the most rules in the last week.
        """
        return User.objects.annotate(total_rules=Count('rules')).filter(
            rules__created_at__gte=self.last_week
        ).order_by('-total_rules')[:limit]

    def get_top_users_rules_last_month(self, limit=3):
        """
        Get the top users who created the most rules in the last month.
        """
        return User.objects.annotate(total_rules=Count('rules')).filter(
            rules__created_at__gte=self.last_month
        ).order_by('-total_rules')[:limit]
        
    def get_top_users_watchers_last_day(self, limit=3):
        """
        Get the top users who created the most watchers in the last day.
        """
        return User.objects.annotate(total_watchers=Count('watchers')).filter(
            watchers__created_at__gte=self.last_day
        ).order_by('-total_watchers')[:limit]

    def get_top_users_watchers_last_week(self, limit=3):
        """
        Get the top users who created the most watchers in the last week.
        """
        return User.objects.annotate(total_watchers=Count('watchers')).filter(
            watchers__created_at__gte=self.last_week
        ).order_by('-total_watchers')[:limit]

    def get_top_users_watchers_last_month(self, limit=3):
        """
        Get the top users who created the most watchers in the last month.
        """
        return User.objects.annotate(total_watchers=Count('watchers')).filter(
            watchers__created_at__gte=self.last_month
        ).order_by('-total_watchers')[:limit]

    def get_top_users_reports_last_day(self, limit=3):
        """
        Get the top users who created the most reports in the last day.
        """
        return User.objects.annotate(total_reports=Count('reports')).filter(
            reports__created_at__gte=self.last_day
        ).order_by('-total_reports')[:limit]

    def get_top_users_reports_last_week(self, limit=3):
        """
        Get the top users who created the most reports in the last week.
        """
        return User.objects.annotate(total_reports=Count('reports')).filter(
            reports__created_at__gte=self.last_week
        ).order_by('-total_reports')[:limit]

    def get_top_users_reports_last_month(self, limit=3):
        """
        Get the top users who created the most reports in the last month.
        """
        return User.objects.annotate(total_reports=Count('reports')).filter(
            reports__created_at__gte=self.last_month
        ).order_by('-total_reports')[:limit]

    def get_rules_by_day_of_week(self):
        """
        Get the number of rules created per day of the week.
        """
        return Rule.objects.filter(created_at__gte=self.start_of_week).values('created_at__week_day').annotate(
            count=Count('id')
        ).order_by('created_at__week_day')
    
    def get_watchers_by_day_of_week(self):
        """
        Get the number of watchers created per day of the week.
        """
        return Watcher.objects.filter(created_at__gte=self.start_of_week).values('created_at__week_day').annotate(
            count=Count('id')
        ).order_by('created_at__week_day')
        
    def get_reports_by_day_of_week(self):
        """
        Get the number of reports created per day of the week.
        """
        return Report.objects.filter(created_at__gte=self.start_of_week).values('created_at__week_day').annotate(
            count=Count('id')
        ).order_by('created_at__week_day')

    def get_total_rules_in_week(self):
        """
        Get the total number of rules created in the current week.
        """
        return Rule.objects.filter(created_at__gte=self.start_of_week).count()
    
    def get_total_watchers_in_week(self):
        """
        Get the total number of watchers created in the current week.
        """
        return Watcher.objects.filter(created_at__gte=self.start_of_week).count()
    
    def get_total_reports_in_week(self):
        """
        Get the total number of reports created in the current week.
        """
        return Report.objects.filter(created_at__gte=self.start_of_week).count()

    def get_detection_system_types(self):
        """
        Get unique detection system types.
        """
        return DetectionSystem.objects.values_list('type', flat=True).distinct()

    def get_rule_counts_by_detection_system(self):
        """
        Get the count of rules per detection system.
        """
        return DetectionSystem.objects.values('type').annotate(rule_count=Count('rules', distinct=True))

    def get_rules_by_month(self):
        """
        Get the number of rules created per month.
        """
        return Rule.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(
            count=Count('id')
        ).order_by('month')

    def get_watchers_by_month(self):
        """
        Get the number of watchers created per month.
        """
        return Watcher.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(
            count=Count('id')
        ).order_by('month')

    def get_reports_by_month(self):
        """
        Get the number of reports created per month.
        """
        return Report.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(
            count=Count('id')
        ).order_by('month')

    def get_total_rules_in_year(self):
        """
        Get the total number of rules created in the current year.
        """
        return Rule.objects.filter(created_at__year=self.current_year).count()
    
    def get_total_watchers_in_year(self):
        """
        Get the total number of watchers created in the current year.
        """
        return Watcher.objects.filter(created_at__year=self.current_year).count()
    
    from django.utils import timezone

    def get_total_reports_in_year(self):
        """
        Get the total number of reports created in the current year.
        """
        return Report.objects.filter(created_at__year=self.current_year).count()

    def get_tactic_ids(self):
        """
        Get the tactic IDs ordered by ID.
        """
        return MitreTactic.objects.values_list('id', flat=True).order_by('id')
    
    def get_tactic_names(self):
        """
        Get the tactic IDs ordered by ID.
        """
        return MitreTactic.objects.values_list('name', flat=True).order_by('id')

    def get_distribution_by_tactic_id(self):
        """
        Get the distribution of rules by MITRE tactic ID.
        """
        return Rule.objects.values('mitre_tactics__id').annotate(count=Count('id')).order_by('mitre_tactics__id')
    
    def get_rules_distribution_by_tactic(self):
        """
        Get the distribution of rules by MITRE tactic.
        """
        tactic_distribution = []

        tactics = MitreTactic.objects.all().order_by('id')
        for tactic in tactics:
            tactic_id = tactic.id
            tactic_name = tactic.name
            rule_count = Rule.objects.filter(mitre_tactics=tactic).count()

            tactic_distribution.append({"mitre_tactic": f"{tactic_id} - {tactic_name}", "rule_count": rule_count})

        return tactic_distribution

    def get_rules_distribution_by_technique(self):
        """
        Get the distribution of rules by MITRE technique.
        """
        technique_distribution = []

        techniques = MitreTechnique.objects.all().order_by('id')
        for technique in techniques:
            technique_id = technique.id
            technique_name = technique.name
            rule_count = Rule.objects.filter(mitre_techniques=technique).count()

            technique_distribution.append({"mitre_technique": f"{technique_id} - {technique_name}", "rule_count": rule_count})

        return technique_distribution

    def get_recent_actions(self, limit=6):
        """
        Get the recent log actions.
        """
        return LogEntry.objects.select_related('user').order_by('-action_time')[:limit]

    def get_rule_counts_by_user(self):
        """
        Get the count of rules created by each user.
        """
        return User.objects.values('username').annotate(rule_count=Count('rules'))

    def get_rule_counts_by_detectionsystem_type(self):
        """
        Get the count of rules created for each detection type.
        """
        return Rule.objects.values('detection_systems__type').annotate(rule_count=Count('id'))
    
    def get_rule_counts_by_detectionsystem_name(self):
        """
        Get the count of rules created for each detection name.
        """
        return Rule.objects.values('detection_systems__name').annotate(rule_count=Count('id')).order_by('-rule_count')
    
    def get_rule_counts_by_technology(self):
        """
        Get the count of rules created for each technology.
        """
        return Rule.objects.values('technologies__name').annotate(rule_count=Count('id')).order_by('-rule_count')

    def get_average_rules_per_user(self):
        """
        Get the average number of rules created per user.
        """
        return User.objects.annotate(rule_count=Count('rules')).aggregate(average=Avg('rule_count'))

    def get_user_with_most_rules(self):
        """
        Get the user with the highest number of created rules.
        """
        return User.objects.annotate(rule_count=Count('rules')).order_by('-rule_count').first()

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
        
    def get_rules_by_detection_system(self, detection_system):
        """
        Get rules grouped by detection system.
        """
        return Rule.objects.filter(detection_system=detection_system)


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

    def get_user_rules(self, user):
        """
        Get the rules created for a specific user.
        """
        return Rule.objects.filter(created_by=user)

    def get_user_watchers(self, user):
        """
        Get the watchers created for a specific user.
        """
        return Watcher.objects.filter(created_by=user)

    def get_user_reports(self, user):
        """
        Get the reports created for a specific user.
        """
        return Report.objects.filter(created_by=user)