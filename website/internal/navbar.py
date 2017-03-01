from flask_nav.elements import View, Subgroup

from utilities.ui.bootstrap import CustomNavbar

internal_navbar = CustomNavbar(
    'IoT',
    [
        View('Home', '.index'),
        View('Help', '.help'),
        View('Themes', '.themes')
    ], [
        View('Help', '.help'),
        Subgroup('Account',
                 View('Settings', '.account_settings'),
                 View('Log out', '.logout')
                 )
    ]
)
