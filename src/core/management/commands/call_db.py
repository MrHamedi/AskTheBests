import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
        Wait until the database is available 
    """
    def handle(self, *args ,**options):
        db_con=None
        while not db_con:
            try:
                db_con=connections["default"]
            except OperationalError:
                self.stdout.write("waiting for database connection...")
                time.sleep(1)
                
        self.stdout.write("database available!")