from datetime import date
from django.core.mail import send_mail
from .models import FD

def check_fd_maturity():
    today = date.today()

    fds = FD.objects.all()

    for fd in fds:
        days_left = (fd.maturity_date - today).days

        print(fd.customer_name, days_left)

        if days_left in [30, 15, 7, 1, 0]:

            print(f"Sending email to {fd.email}")

            try:
                send_mail(
                    "FD Maturity Reminder",
                    f"Dear {fd.customer_name}, your FD {fd.fd_number} matures in {days_left} day(s).",
                    "varuntalwai2020@gmail.com",
                    [fd.email],
                    fail_silently=False,
                )

                print(f"Email sent to {fd.email}")

            except Exception as e:
                print(f"Email failed: {e}")