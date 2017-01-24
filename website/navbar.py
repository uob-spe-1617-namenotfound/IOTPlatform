from flask_nav.elements import View, Navbar, Subgroup

navbar = Navbar(
    'IoT',
    View('Home', '.index'),
    Subgroup('Account',
             View('Settings', '.account_settings'),
             View('Log out', '.logout')
             ),
    View('Help', '.help'),
    View('Themes', '.themes'),
    View('Admin', '.admin')
)
