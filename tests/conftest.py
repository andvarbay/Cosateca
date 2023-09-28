import json
from mysqlx import Client
import pytest

from cosateca import settings

    
@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        "ATOMIC_REQUESTS": True,
    }