from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import PrclientAPIKey

class HasPrclientAPIKey(BaseHasAPIKey):
    model = PrclientAPIKey
