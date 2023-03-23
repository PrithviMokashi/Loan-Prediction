from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=45)
    fname = models.CharField(max_length=45)
    lname = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    passwd = models.CharField(max_length=8)

class LoanData(models.Model):
    userid = models.CharField(max_length=45, default=None)
    loanlimit = models.CharField(max_length=45, default=0)
    gender = models.CharField(max_length=45)
    approve = models.CharField(max_length=45)
    loantype = models.CharField(max_length=45)
    negammor = models.CharField(max_length=45)
    intonly = models.CharField(max_length=45)
    lumpsum = models.CharField(max_length=45)
    propertyvalue = models.CharField(max_length=45)
    consttype = models.CharField(max_length=45)
    occupancytype = models.CharField(max_length=45)
    securedby = models.CharField(max_length=45)
    totalunits = models.CharField(max_length=45)
    income = models.CharField(max_length=45)
    credittype = models.CharField(max_length=45)
    creditscore = models.CharField(max_length=45)
    securitytype = models.CharField(max_length=45)
    loanpurpose = models.CharField(max_length=45)
    credworthiness = models.CharField(max_length=45)
    opencredit = models.CharField(max_length=45)
    business = models.CharField(max_length=45)
    loanamount = models.CharField(max_length=45)
    rateinterest = models.CharField(max_length=45)
    intratespread = models.CharField(max_length=45)
    upfrontcharges = models.CharField(max_length=45)
    term = models.CharField(max_length=45)
    cocredtype = models.CharField(max_length=45)
    age = models.CharField(max_length=45)
    appsub = models.CharField(max_length=45)
    loantoval = models.CharField(max_length=45)
    region = models.CharField(max_length=45)
    deptincratio = models.CharField(max_length=45)
