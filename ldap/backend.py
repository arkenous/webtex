from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from ldap3 import Server, Connection, SIMPLE
from ldap3.core.exceptions import LDAPBindError


class LDAPBackend(object):
    @staticmethod
    def authenticate(username=None, password=None):
        s = Server(host=settings.LDAP_SERVER_ADDRESS,
                   port=settings.LDAP_SERVER_PORT)

        user_dn = 'uid='+username+','+settings.LDAP_USER_BASEDN

        try:
            c = Connection(server=s,
                           user=user_dn,
                           password=password,
                           authentication=SIMPLE,
                           check_names=True,
                           auto_bind=True)
            user = get_user_model()

            result, created = user.objects.update_or_create(
                username=username,
                password=password
            )

            c.unbind()
            return result
        except LDAPBindError:
            return None

    @staticmethod
    def get_user(user_id):
        user = get_user_model()
        try:
            return user.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
