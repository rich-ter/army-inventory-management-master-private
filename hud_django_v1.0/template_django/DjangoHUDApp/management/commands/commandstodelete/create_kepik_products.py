import json
from django.core.management.base import BaseCommand
from DjangoHUDApp.models import Product, Warehouse, Stock, Group
from DjangoHUDApp.models import Product, ProductCategory, ProductUsage

class Command(BaseCommand):
    help = 'Load products into the Kepik warehouse from a JSON file'

    def handle(self, *args, **kwargs):

        # Ensure the ΔΙΔΕΣ group exists
        dides_group, _ = Group.objects.get_or_create(name='ΔΙΔΕΣ')

        category_kamia_epilogi = ProductCategory.objects.get(name="ΚΑΜΙΑ ΕΠΙΛΟΓΗ")
        usage_kamia_epilogi = ProductUsage.objects.get(name="ΚΑΜΙΑ ΕΠΙΛΟΓΗ")

        try:
            kepik_warehouse = Warehouse.objects.get(name='ΚΕΠΙΚ')
        except Warehouse.DoesNotExist:
            self.stdout.write(self.style.ERROR('Kepik warehouse does not exist.'))
            return
        
        # The product data to be loaded
        kepik_products = [
            {"Α/Α": "1", "name": "CISCO 871", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "2"},
            {"Α/Α": "2", "name": "CISCO 1751", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "3", "name": "CISCO 2600", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "ΚΕΠΠΕΑ", "ΣΥΝΟΛΟ": "2"},
            {"Α/Α": "4", "name": "CISCO 3600", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "5", "name": "PANDATEL 64 Kbps", "category": "CONVERTER", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "2"},
            {"Α/Α": "6", "name": "Combiner", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "7", "name": "CISCO 2911", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "2"},
            {"Α/Α": "8", "name": "CISCO 1941", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "9", "name": "CISCO 1921", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Προμήθεια από το 487 ΤΔΒ. Αναμονή δγής διάθεσης σε Σχηματισμούς – Μονάδες από ΓΕΣ/ΔΔΒ", "ΣΥΝΟΛΟ": "18"},
            {"Α/Α": "10", "name": "ALCATEL SWITCH 48 Port", "category": "SWITCH", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "2"},
            {"Α/Α": "11", "name": "SWITCH 2960C - 8TC-S", "category": "SWITCH", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Προμήθεια από το 487 ΤΔΒ. Αναμονή δγής διάθεσης σε Σχηματισμούς – Μονάδες από ΓΕΣ/ΔΔΒ", "ΣΥΝΟΛΟ": "7"},
            {"Α/Α": "12", "name": "SWITCH 2960C - 24TC-S", "category": "SWITCH", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Προμήθεια από το 487 ΤΔΒ. Αναμονή δγής διάθεσης σε Σχηματισμούς – Μονάδες από ΓΕΣ/ΔΔΒ", "ΣΥΝΟΛΟ": "21"},
            {"Α/Α": "13", "name": "Κάρτα HWIC – 1ADSL", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "36"},
            {"Α/Α": "14", "name": "Κάρτα HWIC - 1T", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "27"},
            {"Α/Α": "15", "name": "Κάρτα WIC - 1T (Παλαιού τύπου)", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Συσκευάζονται στο ίδιο κουτί", "ΣΥΝΟΛΟ": "10"},
            {"Α/Α": "16", "name": "Κάρτα WIC - 2T", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Συσκευάζονται στο ίδιο κουτί", "ΣΥΝΟΛΟ": "5"},
            {"Α/Α": "17", "name": "Κάρτα VIC 3 – 4 FXS / DID", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Συσκευάζονται στο ίδιο κουτί", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "18", "name": "Κάρτα VIC 3 – 2 FXS / DID", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Συσκευάζονται στο ίδιο κουτί", "ΣΥΝΟΛΟ": "9"},
            {"Α/Α": "19", "name": "Κάρτα VIC 3 – 4 FXS / DID", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Συσκευάζονται στο ίδιο κουτί", "ΣΥΝΟΛΟ": "3"},
            {"Α/Α": "20", "name": "Κάρτα VIC 3 – 2 FXS / DID", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Συσκευάζονται στο ίδιο κουτί", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "21", "name": "Κάρτα VIC 2– 2 FXO", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Συσκευάζονται στο ίδιο κουτί", "ΣΥΝΟΛΟ": "4"},
            {"Α/Α": "22", "name": "Κάρτα VIC 2– 4 FXO", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Συσκευάζονται στο ίδιο κουτί", "ΣΥΝΟΛΟ": "5"},
            {"Α/Α": "23", "name": "Κάρτα EHWIC – 4 ESG", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "8"},
            {"Α/Α": "24", "name": "Κάρτα PVDM 3-16", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "5"},
            {"Α/Α": "25", "name": "Κάρτα PVDM 2-8", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "8"},
            {"Α/Α": "26", "name": "Τροφοδοτικά Cisco 2800", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "2"},
            {"Α/Α": "27", "name": "Κάρτα BRI 8B- S/T", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "28", "name": "Κάρτα WIC 1 AM V2", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "29", "name": "Κάρτα 1B- S/T", "category": "MODULE", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "3"},
            {"Α/Α": "30", "name": "FAST ETHERNET MEDIA CONVERTER", "category": "ΜΕΤΑΤΡΟΠΕΑΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "27"},
            {"Α/Α": "31", "name": "Allied Telesis Extended Ethernet", "category": "LAN EXTENDER", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "80"},
            {"Α/Α": "32", "name": "ALCATEL ROUTER", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "13"},
            {"Α/Α": "33", "name": "Καλώδια Τροφοδοσίας", "category": "ΚΑΛΩΔΙΩΣΗ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "2 (Κουτιά)", "ΣΥΝΟΛΟ": "2"},
            {"Α/Α": "34", "name": "Καλώδια κονσόλας", "category": "ΚΑΛΩΔΙΩΣΗ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "1 (Κουτί)", "ΣΥΝΟΛΟ": "1"},
            {"Α/Α": "35", "name": "Καλώδια V35-Smart serial", "category": "ΚΑΛΩΔΙΩΣΗ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "19"},
            {"Α/Α": "36", "name": "Καλώδια X21-Smart serial", "category": "ΚΑΛΩΔΙΩΣΗ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "43"},
            {"Α/Α": "37", "name": "Καλώδια RS530-Smart serial", "category": "ΚΑΛΩΔΙΩΣΗ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "8"},
            {"Α/Α": "38", "name": "Καλώδια RS232-Smart serial", "category": "ΚΑΛΩΔΙΩΣΗ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "47"},
            {"Α/Α": "39", "name": "Καλώδια BNC - RJ 45", "category": "ΚΑΛΩΔΙΩΣΗ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "39"},
            {"Α/Α": "40", "name": "Racks", "category": "RACK", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "6"},
            {"Α/Α": "41", "name": "PANDATEL", "category": "MODEM", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "6"},
            {"Α/Α": "42", "name": "PANDACOM", "category": "MODEM", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "34"},
            {"Α/Α": "43", "name": "Μετατροπείς G703-X21", "category": "ΜΕΤΑΤΡΟΠΕΑΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "", "ΣΥΝΟΛΟ": "8"},
            {"Α/Α": "44", "name": "VTC LIFESIZE 50", "category": "ΣΥΣΤΗΜΑ ΤΗΛΕΔΙΑΣΚΕΨΗΣ", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "Αναμονή δγή διάθεσης – κατανομής από ΓΕΣ/ΔΔΒ", "ΣΥΝΟΛΟ": "9"},
            {"Α/Α": "45", "name": "Ανυψωτήρες Rack", "category": "RACK", "usage": "ΔΙΔΕΣ ΔΙΚΤΥΑΚΟΣ ΕΞΟΠΛΙΣΜΟΣ", "description": "54(Κουτιά)", "ΣΥΝΟΛΟ": "54"},
            {"Α/Α": "46", "name": "LG LED MONITOR 19’’", "category": "ΟΘΟΝΗ", "usage": "ΣΔΑ ΠΥΡΣΕΙΑ", "description": "", "ΣΥΝΟΛΟ": "18"},
            {"Α/Α": "47", "name": "H/Y QUEST", "category": "ΥΠΟΛΟΓΙΣΤΗΣ", "usage": "ΣΔΑ ΠΥΡΣΕΙΑ", "description": "", "ΣΥΝΟΛΟ": "18"},
            {"Α/Α": "48", "name": "ΕΞΩΤΕΡΙΚΕΣ ΔΙΣΚΕΤΕΣ", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΣΔΑ ΠΥΡΣΕΙΑ", "description": "", "ΣΥΝΟΛΟ": "32"},
            {"Α/Α": "49", "name": "HD 500G", "category": "ΕΞΩΤΕΡΙΚΟΙ ΔΙΣΚΟΙ", "usage": "ΣΔΑ ΠΥΡΣΕΙΑ", "description": "", "ΣΥΝΟΛΟ": "20"},
            {"Α/Α": 50, "name": "USB FLASH DRIVE", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΣΔΑ ΠΥΡΣΕΙΑ", "description": "Σε εξέλιξη ενέργεια του ΓΕΣ/ΔΔΒ για κρυπτασφάλιση και διανομή σε Μονάδες", "Ποσότητα": 1761},
            {"Α/Α": 51, "name": "SERVER HP DL 380", "category": "ΕΞΥΠΗΡΕΤΗΤΕΣ", "usage": "ΣΔΑ ΠΥΡΣΕΙΑ", "description": "Χωρίς Τροφοδοτικά (Καμένα)", "Ποσότητα": 2},
            {"Α/Α": 52, "name": "Microtek ScanMaker (A3)", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΣΔΑ ΠΥΡΣΕΙΑ", "Ποσότητα": 7},
            {"Α/Α": 53, "name": "GIGASET DA 610", "category": "ΤΗΛΕΦΩΝΙΚΗ ΣΥΣΚΕΥΗ", "usage": "ΕΨΑΔ-ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ", "Ποσότητα": 50},
            {"Α/Α": 54, "name": "GIGASET NEC", "category": "ΤΗΛΕΦΩΝΙΚΗ ΣΥΣΚΕΥΗ", "usage": "ΕΨΑΔ-ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ αναλογικές", "Ποσότητα": 50},
            {"Α/Α": 55, "name": "ALCATEL 4035", "category": "ΤΗΛΕΦΩΝΙΚΗ ΣΥΣΚΕΥΗ", "usage": "ΕΨΑΔ-ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ", "Ποσότητα": 15},
            {"Α/Α": 56, "name": "ALCATEL 4010", "category": "ΤΗΛΕΦΩΝΙΚΗ ΣΥΣΚΕΥΗ", "usage": "ΕΨΑΔ-ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ", "Ποσότητα": 2},
            {"Α/Α": 57, "name": "Οθόνη IBM Τηλ.Κέντρου", "category": "ΟΘΟΝΗ", "usage": "ΕΨΑΔ-ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ", "Ποσότητα": 1},
            {"Α/Α": 58, "name": "Εξυπηρετητής IBM Τηλ.Κέντρου", "category": "ΕΞΥΠΗΡΕΤΗΤΕΣ", "usage": "ΕΨΑΔ-ΤΗΛΕΦΩΝΙΚΟ ΚΕΝΤΡΟ", "Ποσότητα": 1},
            {"Α/Α": 59, "name": "Πολυμηχανήμα LEXMARK Χ204Ν", "category": "ΕΚΤΥΠΩΤΗΣ", "usage": "ΚΡΥΠΤΟ", "Ποσότητα": 2},
            {"Α/Α": 60, "name": "DELL Οθόνες", "category": "ΟΘΟΝΗ", "usage": "ΚΡΥΠΤΟ", "description": "Οι κεντρικές μονάδες βρίσκονται στο Control Room για ανάγκες κρυπτοτηλεφωνίας. Στην αποθήκη βρίσκονται μόνο οι αντίστοιχες 29 οθόνες", "Ποσότητα": 29},
            {"Α/Α": 61, "name": "MGE Pulsar Extreme 1000", "category": "UPS", "usage": "UPS", "Ποσότητα": 1},
            {"Α/Α": 62, "name": "APC Smart Ups 1400 XL", "category": "UPS", "usage": "UPS", "Ποσότητα": 1},
            {"Α/Α": 63, "name": "Κομμάτια αντιστατικού Δαπέδου", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 18},
            {"Α/Α": 64, "name": "INTRACOM RCE", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 4},
            {"Α/Α": 65, "name": "Οθόνη HP W1972", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 66, "name": "Πολυμηχανήμα Officejet", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ"},
            {"Α/Α": 67, "name": "CISCO Router 1601", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 68, "name": "CISCO Router 1751", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 69, "name": "CISCO Router 1720", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 2},
            {"Α/Α": 70, "name": "CISCO Router 3600", "category": "ΔΡΟΜΟΛΟΓΗΤΗΣ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 3},
            {"Α/Α": 71, "name": "Υπολογιστής HP COMPAQ", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 72, "name": "Κάρτα VIC 2FXS", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 73, "name": "Κάρτα VIC 3 – 4 FXS / DID", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 74, "name": "Κάρτα VWIC 1MFT – T1/E1", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 75, "name": "Κάρτα WIC 2 A/S", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 2},
            {"Α/Α": 76, "name": "Κάρτα VWIC2 2MFT – G703", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 77, "name": "Κάρτα WIC - 2T", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 78, "name": "Κάρτα VWIC2 2MFT – T1/E1", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 79, "name": "Module 2W", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 80, "name": "Module Voice 2V", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 81, "name": "PANDATEL", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 5},
            {"Α/Α": 82, "name": "ULAF Siemens", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 3},
            {"Α/Α": 83, "name": "ALCATEL Modem", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 84, "name": "PANDATEL 64 Kbps", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 4},
            {"Α/Α": 85, "name": "Τροφοδοτικό Cisco 2800", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 86, "name": "Οθόνη PHILIPS 170 C", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 87, "name": "Οθόνη PHILIPS 190 WV", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
            {"Α/Α": 88, "name": "Οθόνη HP 1730", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 3},
            {"Α/Α": 89, "name": "Οθόνη L170 C", "category": "ΛΟΙΠΑ ΥΛΙΚΑ", "usage": "ΚΑΜΙΑ ΕΠΙΛΟΓΗ", "Ποσότητα": 1},
        ]

        # Process each product and assign it to the group and warehouse
        for item in kepik_products:
            # Create or get the product
            product, created = Product.objects.get_or_create(
                name=item["name"],
                defaults={
                    'category': category_kamia_epilogi,
                    'usage': usage_kamia_epilogi,
                    'description': item.get("description", ""),
                    # 'batch_number': item["batch_number"],  # Use the provided batch_number
                    'unit_of_measurement': 'ΚΑΜΙΑ ΕΠΙΛΟΓΗ' # Use the provided unit_of_measurement
                }
            )

            # Add the ΔΙΔΕΣ group to the product owners if the product was newly created
            if created:
                product.owners.add(dides_group)
                product.save()

            # Create or update the stock in the "Kepik Warehouse"
            # stock, _ = Stock.objects.get_or_create(product=product, warehouse=kepik_warehouse, defaults={'quantity': item["quantity"]})
            # stock.quantity = item["quantity"]
            # stock.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded Kepik products into the database'))