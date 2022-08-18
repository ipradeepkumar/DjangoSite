import os
from django_python3_ldap.utils import format_search_filters
from django.contrib.auth.decorators import login_required, user_passes_test
def is_authenticated(self, ldap_fields):
     # Add in simple filters.
    ldap_fields["username"] = os.getlogin()
    # Call the base format callable.
    search_filters = format_search_filters(ldap_fields)
    return (search_filters.count > 0)

ldap_user_exists = user_passes_test(lambda u: True if u.is_authenticated else False, login_url='login')

def ldap_auth(view_func):
    decorated_view_func = login_required(ldap_user_exists(view_func), login_url='login')
    return decorated_view_func

