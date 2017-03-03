from flask_nav.elements import View, Subgroup
from utilities.ui.bootstrap import CustomNavbar


public_navbar = CustomNavbar(
    'IoT',
    [
        View('Home', 'public.index'),
    ], [
        View('Help', 'public.help'),
        Subgroup('Account',
                 View('Register', 'public.register'),
                 View('Sign in', 'public.login')
                 )
    ]
)