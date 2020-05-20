from django_auth_ldap.backend import LDAPBackend
from django.contrib.auth import get_user_model

class StoreLDAPBackend(LDAPBackend):

    def authenticate(self, request, username, password, **kwargs):
        """ Overrides LDAPBackend.authenticate to save user password in Django in case LDAP server is not available """

        user = super().authenticate(request, username, password, **kwargs)

        # if login successful
        if user:
            user.set_password(password)
            user.save()

        return user
