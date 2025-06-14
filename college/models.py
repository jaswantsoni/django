from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class College(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='colleges')
    college_name = models.CharField(max_length=200)
    overall_cgpa = models.FloatField()

    def __str__(self):
        return f"{self.college_name} ({self.user})"

class Banking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bank_accounts')
    banking_name = models.CharField(max_length=200)
    account_number = models.CharField(max_length=50)
    balance = models.FloatField()

    def __str__(self):
        return f"{self.banking_name} ({self.user})"
