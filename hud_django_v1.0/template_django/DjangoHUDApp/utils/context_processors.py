from django.urls import resolve, reverse, Resolver404

def mark_active_link(menu, current_path, current_view_name, current_kwargs):
    for item in menu:
        # Compare URL or use the view name with kwargs
        if 'name' in item:
            try:
                item_view_name = resolve(item['url']).url_name
                if item_view_name == current_view_name:
                    if item_view_name == 'pageStockPerWarehouse':
                        # Check if the warehouse name parameter matches
                        if 'warehouse_name' in current_kwargs and 'warehouse_name' in item['kwargs']:
                            item['is_active'] = item['kwargs']['warehouse_name'] == current_kwargs['warehouse_name']
                        else:
                            item['is_active'] = False
                    else:
                        item['is_active'] = True
                else:
                    item['is_active'] = False
            except Resolver404:
                item['is_active'] = False
        else:
            item['is_active'] = item.get('url', '') == current_path

        if 'children' in item:
            item['children'] = mark_active_link(item['children'], current_path, current_view_name, current_kwargs)

            if any(child.get('is_active', False) for child in item['children']):
                item['is_active'] = True

    return menu

def sidebar_menu(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)

    sidebar_menu = [{
        'text': 'Επιλογές',
        'is_header': 1
    }, {
        'url': reverse('DjangoHUDApp:index'),
        'icon': 'bi bi-cpu',
        'text': 'Πίνακας Ελέγχου',
        'name': 'index',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'is_divider': 1
    }, {
        'text': 'Ενέργειες Προιόντων',
        'is_header': 1,
        'css_class': 'text-success fw-bold'
    }, {
        'url': reverse('DjangoHUDApp:pageProduct'),
        'icon': 'fas fa-tags',
        'text': 'Λίστα Προιόντων',
        'name': 'pageProduct',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'url': reverse('DjangoHUDApp:add_product'),
        'icon': 'fas fa-plus',
        'text': 'Προσθήκη Προιόντος',
        'name': 'add_product',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'url': reverse('DjangoHUDApp:pageDataManagement'),
        'icon': 'fas fa-barcode',
        'text': 'Αποθέματα',
        'name': 'pageDataManagement',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'is_divider': 1
    }, {
        'text': 'Ενέργιες Διακινίσεων',
        'is_header': 1,
        'css_class': 'text-success fw-bold'
    }, {
        'url': reverse('DjangoHUDApp:pageOrder'),
        'icon': 'bi bi-layout-sidebar',
        'text': 'Λίστα Διακινίσεων',
        'name': 'pageOrder',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'url': reverse('DjangoHUDApp:add_shipment'),
        'icon': 'far fa-envelope',
        'text': 'Δημιουργία Διακίνησης',
        'name': 'add_shipment',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'url': reverse('DjangoHUDApp:pageRecipient'),
        'icon': 'far fa-address-book',
        'text': 'Παραλήπτες',
        'name': 'pageRecipient',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'is_divider': 1
    }, {
        'text': 'Ενέργειες Αποθηκών',
        'is_header': 1,
        'css_class': 'text-success fw-bold'
    }, {
        'url': reverse('DjangoHUDApp:pageWarehouse'),
        'icon': 'fas fa-cubes',
        'text': 'Λίστα Αποθηκών',
        'name': 'pageWarehouse',
        'groups': ['ΔΙΔΕΣ', 'admin']
    }, {
        'url': reverse('DjangoHUDApp:pageStockPerWarehouse', kwargs={'warehouse_name': 'ΚΕΠΙΚ'}),
        'icon': 'fas fa-server',
        'text': 'Αποθήκη ΚΕΠΙΚ',
        'name': 'pageStockPerWarehouse',
        'kwargs': {'warehouse_name': 'ΚΕΠΙΚ'},
        'groups': ['ΔΙΔΕΣ', 'admin']
    }, {
        'url': reverse('DjangoHUDApp:pageStockPerWarehouse', kwargs={'warehouse_name': 'ΤΑΓΜΑ'}),
        'icon': 'fas fa-building',
        'text': 'Αποθήκη Τάγματος',
        'name': 'pageStockPerWarehouse',
        'kwargs': {'warehouse_name': 'ΤΑΓΜΑ'},
        'groups': ['ΔΙΔΕΣ', 'admin']
    }, {
        'url': reverse('DjangoHUDApp:pageStockPerWarehouse', kwargs={'warehouse_name': 'ΔΟΡΥΦΟΡΙΚΑ'}),
        'icon': 'fas fa-signal',
        'text': 'Αποθήκη Δορυφορικών',
        'name': 'pageStockPerWarehouse',
        'kwargs': {'warehouse_name': 'ΔΟΡΥΦΟΡΙΚΑ'},
        'groups': ['ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'is_divider': 1
    }, {
        'text': 'Άλλες Ενέργειες',
        'is_header': 1,
        'css_class': 'text-success fw-bold'
    }, {
        'url': reverse('DjangoHUDApp:logout'),
        'icon': 'bi bi-people',
        'text': 'Έξοδος',
        'name': 'logout',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }]
    
    # Filter menu items based on user groups or if user is an admin
    filtered_menu = []
    for item in sidebar_menu:
        if 'groups' in item:
            if 'admin' in item['groups'] and user.is_superuser:
                filtered_menu.append(item)
            elif any(group in user_groups for group in item['groups']):
                filtered_menu.append(item)
        else:
            filtered_menu.append(item)

    current_full_path = request.path
    resolved_path = resolve(request.path_info)
    current_view_name = resolved_path.url_name
    current_kwargs = resolved_path.kwargs
    filtered_menu = mark_active_link(filtered_menu, current_full_path, current_view_name, current_kwargs)

    return {'sidebar_menu': filtered_menu}
