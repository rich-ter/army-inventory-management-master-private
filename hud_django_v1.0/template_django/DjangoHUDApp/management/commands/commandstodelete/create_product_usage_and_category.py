from django.core.management.base import BaseCommand
from DjangoHUDApp.models import ProductCategory, ProductUsage

class Command(BaseCommand):
    help = 'Populate initial product categories and usages'

    def handle(self, *args, **kwargs):
        categories = [
            "ΔΡΟΜΟΛΟΓΗΤΗΣ",
            "CONVERTER",
            "SWITCH",
            "MODULES",
            "ΜΕΤΑΤΡΟΠΕΑΣ",
            "LAN EXTENDER",
            "ΚΑΛΩΔΙΩΣΗ",
            "ΛΟΙΠΑ ΥΛΙΚΑ",
            "IP PHONES",
            "MODULE",
            "RACK",
            "MODEM",
            "ΣΥΣΤΗΜΑ ΤΗΛΕΔΙΑΣΚΕΨΗΣ",
            "ΥΠΟΛΟΓΙΣΤΗΣ",
            "ΕΞΩΤΕΡΙΚΟΙ ΔΙΣΚΟΙ",
            "ΕΞΥΠΗΡΕΤΗΤΕΣ",
            "ΤΗΛΕΦΩΝΙΚΗ ΣΥΣΚΕΥΗ",
            "ΟΘΟΝΗ",
            "ΕΚΤΥΠΩΤΗΣ",
            "UPS",
            "ΚΑΜΙΑ ΕΠΙΛΟΓΗ",
        ]

        usages = [
            "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ",
            "ΣΔΑ ΠΥΡΣΕΙΑ",
            "ΕΨΑΔ-ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ",
            "ΚΡΥΠΤΟ",
            "UPS",
            "ΔΟΡΥΦΟΡΙΚΑ",
            "ΕΨΑΔ-ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ αναλογικές",
            "ΚΑΜΙΑ ΕΠΙΛΟΓΗ",
        ]

        for category in categories:
            ProductCategory.objects.get_or_create(name=category)
        
        for usage in usages:
            ProductUsage.objects.get_or_create(name=usage)

        self.stdout.write(self.style.SUCCESS('Successfully populated product categories and usages'))
