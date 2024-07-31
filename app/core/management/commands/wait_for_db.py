""" 
Django command ot wait for the dartabsae to abe available 
"""
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self,*args,**options):
        pass