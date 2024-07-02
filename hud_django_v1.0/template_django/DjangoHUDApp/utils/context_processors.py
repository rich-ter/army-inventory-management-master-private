from django.urls import resolve

def mark_active_link(menu, current_path_name):
    for item in menu:
        item['is_active'] = item.get('name', '') == current_path_name

        if 'children' in item:
            item['children'] = mark_active_link(item['children'], current_path_name)

            if any(child.get('is_active', False) for child in item['children']):
                item['is_active'] = True

    return menu

def sidebar_menu(request):
    user = request.user
    user_groups = user.groups.values_list('name', flat=True)
    
    # Define the sidebar menu
    sidebar_menu = [{
        'text': 'Επιλογές',
        'is_header': 1
    }, {
        'url': '/index',
        'icon': 'bi bi-cpu',
        'text': 'Πίνακας Ελέγχου',
        'name': 'index',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']  # Specify groups and admin that can see this item
    }, {
        'is_divider': 1
    }, {
        'text': 'Ενέργειες Προιόντων',
        'is_header': 1
    }, {
        'url': '/all-products',
        'icon': 'fas fa-tags',
        'text': 'Λίστα Προιόντων',
        'name': 'pageProduct',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'url': '/add-product',
        'icon': 'fas fa-plus',
        'text': 'Προσθήκη Προιόντος',
        'name': 'dashboard',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'url': '/stock',
        'icon': 'fas fa-barcode',
        'text': 'Αποθέματα',
        'name': 'pageDataManagement',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'is_divider': 1
    }, {
        'text': 'Ενέργιες Διακινίσεων',
        'is_header': 1
    }, {
        'url': '/order',
        'icon': 'bi bi-layout-sidebar',
        'text': 'Λίστα Διακινίσεων',
        'name': '',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'url': '/add-shipment',
        'icon': 'far fa-envelope',
        'text': 'Δημιουργία Διακίνισης',
        'name': 'dashboard',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'url': '/recipient',
        'icon': 'far fa-address-book',
        'text': 'Παραλήπτες',
        'name': 'dashboard',
        'groups': ['ΔΙΔΕΣ', 'ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'is_divider': 1
    }, {
        'text': 'Ενέργειες Αποθηκών',
        'is_header': 1
    }, {
        'url': '/warehouse',
        'icon': 'fas fa-cubes',
        'text': 'Λίστα Αποθηκών',
        'name': 'dashboard',
        'groups': ['ΔΙΔΕΣ', 'admin']
    }, {
        'url': '/stock-per-warehouse/ΚΕΠΙΚ',
        'icon': 'fas fa-server',
        'text': 'Αποθήκη ΚΕΠΙΚ',
        'name': 'dashboard',
        'groups': ['ΔΙΔΕΣ', 'admin']
    }, {
        'url': '/stock-per-warehouse/ΤΑΓΜΑ',
        'icon': 'fas fa-building',
        'text': 'Αποθήκη Τάγματος',
        'name': 'dashboard',
        'groups': ['ΔΙΔΕΣ', 'admin']
    }, {
        'url': '/stock-per-warehouse/ΔΟΡΥΦΟΡΙΚΑ',
        'icon': 'fas fa-signal',
        'text': 'Αποθήκη Δορυφορικών',
        'name': 'dashboard',
        'groups': ['ΔΟΡΥΦΟΡΙΚΑ', 'admin']
    }, {
        'is_divider': 1
    }, {
        'text': 'Άλλες Ενέργειες',
        'is_header': 1
    }, {
        'url': '/logout',
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

    resolved_path = resolve(request.path_info)
    current_path_name = resolved_path.url_name
    filtered_menu = mark_active_link(filtered_menu, current_path_name)

    return {'sidebar_menu': filtered_menu}
