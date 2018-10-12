from django.core.management.base import BaseCommand
from main.cron_jobs import do_hourly_job


class Command(BaseCommand):
    help = "Lifemark app's hourly job for crontab"

    def handle(self, *args, **options):
        do_hourly_job()
