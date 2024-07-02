from django import template

register = template.Library()

@register.inclusion_tag('filters/products-search-form.html', takes_context=True)
def render_product_filter_form(context, filter):
    return {'filter': filter}

@register.inclusion_tag('filters/shipments-search-form.html', takes_context=True)
def render_shipment_filter_form(context, filter):
    return {'filter': filter}

@register.inclusion_tag('filters/recipients-search-form.html', takes_context=True)
def render_recipients_filter_form(context, filter):
    return {'filter': filter}

@register.inclusion_tag('filters/stock-search-form.html', takes_context=True)
def render_stock_filter_form(context, filter):
    return {'filter': filter}