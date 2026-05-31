
from django.db import models
from django.contrib.auth.models import User


class FD(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    bank_name = models.CharField(max_length=100)
    fd_number = models.CharField(max_length=50)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    start_date = models.DateField()
    maturity_date = models.DateField()

    # Reminder tracking
    reminder_30_sent = models.BooleanField(default=False)
    reminder_15_sent = models.BooleanField(default=False)
    reminder_7_sent = models.BooleanField(default=False)
    reminder_1_sent = models.BooleanField(default=False)
    reminder_0_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name

    def maturity_amount(self):
        years = (self.maturity_date - self.start_date).days / 365

        return round(
            float(self.amount) *
            ((1 + float(self.interest_rate) / 100) ** years),
            2
        )