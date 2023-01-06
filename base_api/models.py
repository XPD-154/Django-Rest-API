from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

# Create your models here.

class Prclient(models.Model):
    clientid = models.AutoField(db_column='clientID', primary_key=True)  # Field name made lowercase.
    clemail = models.CharField(db_column='CLemail', max_length=50)  # Field name made lowercase.
    clpassword = models.CharField(db_column='CLpassword', max_length=50)  # Field name made lowercase.
    clcompany_name = models.CharField(db_column='CLcompany_name', max_length=50)  # Field name made lowercase.
    clphone_number = models.CharField(db_column='CLphone_number', max_length=50)  # Field name made lowercase.
    cluniqueid = models.CharField(db_column='CLuniqueId', max_length=50, unique=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'prclient'

class PrclientAPIKey(AbstractAPIKey):
    client_key = models.ForeignKey(Prclient, on_delete=models.CASCADE)
