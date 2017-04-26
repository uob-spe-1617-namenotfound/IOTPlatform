from flask_nav.elements import View, Subgroup

from utilities.ui.bootstrap import CustomNavbar

internal_navbar = CustomNavbar(

    'IoT',
    [
        View('Home', '.index'),
        View('All devices', '.show_devices'),
        Subgroup('More',
                 View('Triggers', '.show_all_triggers'),
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
