# your_app/templatetags/date_filters.py

from django import template

register = template.Library()

MONTHS_EN_TO_GR = {
    1: 'Ιανουαρίου',
    2: 'Φεβρουαρίου',
    3: 'Μαρτίου',
    4: 'Απριλίου',
    5: 'Μαίου',
    6: 'Ιουνίου',
    7: 'Ιουλίου',
    8: 'Αυγούστου',
    9: 'Σεπτεμβρίου',
    10: 'Οκτωβρίου',
    11: 'Νοεμβρίου',
    12: 'Δεκεμβρίου'
}

@register.filter
def greek_month(date):
    month_number = date.month
    return MONTHS_EN_TO_GR.get(month_number, 'Unknown')
