from flask_nav.elements import Subgroup, View

from utilities.ui.bootstrap import CustomNavbar

admin_navbar = CustomNavbar(
    'IoT ADMIN',
    [
        View('Home', '.index'),
    ], [
        Subgroup('Account',
                 View('Settings', '.index'),
                 View('Logout', '.logout'),
                 ),
    ]
)
