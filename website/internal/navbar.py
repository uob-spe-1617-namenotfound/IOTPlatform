from flask_nav.elements import View, Subgroup

from utilities.ui.bootstrap import CustomNavbar

internal_navbar = CustomNavbar(

    'IoT',
    [
        View('Home', '.index'),
        Subgroup('Devices',
                 View('All Devices','.show_devices'),
                 View('Themes', '.themes'),
                 View('Graph', '.graph')
                 )
    ], [
        View('Help', '.help'),
        Subgroup('Account',
                 View('Settings', '.account_settings'),
                 View('Log out', '.logout')
                 )
    ]
)
