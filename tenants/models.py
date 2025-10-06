from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from django.contrib.auth.models import User
from django_tenants.utils import schema_context, get_public_schema_name
from datetime import date, timedelta

def get_default_paid_until():
    return date.today() + timedelta(days=365)

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until = models.DateField(default=get_default_paid_until)
    on_trial = models.BooleanField(default=True)

    auto_create_schema = True  # important: creates schema automatically

class Domain(DomainMixin):
    pass
