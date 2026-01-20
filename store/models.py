from django.db import models

class user(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    pwd = models.CharField(max_length=50)
    phno = models.IntegerField()

    class Meta:
        db_table = "user"

class student(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    pincode = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    fathername = models.CharField(max_length=50)
    mothername = models.CharField(max_length=50)
    phno = models.IntegerField()
    email = models.EmailField()
    aadharno = models.IntegerField()
    age = models.IntegerField()

    class Meta:
        db_table = "student"

class picfile(models.Model):
    fname = models.CharField(max_length=50)
    furl = models.ImageField()

    class Meta:
        db_table = "picfile"
