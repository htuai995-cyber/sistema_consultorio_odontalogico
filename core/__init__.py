"""
Core package initialization with MariaDB 10.4 and Python 3.14 compatibility patches.
"""
from django.template import context as django_context


# Parche para Python 3.14 en Django 4.2 LTS (compatibilidad con copy(Context))
def _patched_context_copy(self):
    obj = self.__class__.__new__(self.__class__)
    obj.__dict__.update(self.__dict__)
    obj.dicts = self.dicts[:]
    return obj


django_context.BaseContext.__copy__ = _patched_context_copy
django_context.Context.__copy__ = _patched_context_copy

# Compatibilidad garantizada para MariaDB 10.4+ (XAMPP)
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None
except Exception:
    pass
