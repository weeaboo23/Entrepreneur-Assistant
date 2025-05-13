from django.core.management.base import BaseCommand
from ai_model import train_model

class Command(BaseCommand):
    help = "Retrain the local AI model using logged examples."

    def handle(self, *args, **kwargs):
        train_model()
        self.stdout.write("🎯 AI model retrained and saved.")