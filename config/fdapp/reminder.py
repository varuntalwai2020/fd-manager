from datetime import date
from django.core.mail import send_mail
from .models import FD

def check_fd_maturity():
    print("=== CHECKING FD MATURITY ===")

    today = date.today()
    print("Today:", today)

    fds = FD.objects.all()
    print("Total FDs:", fds.count())

    for fd in fds:
        print("PROCESSING:", fd.customer_name)
        days_left = (fd.maturity_date - today).days
        print("DAYS LEFT =", days_left)

        print(
            f"Customer={fd.customer_name}, "
            f"Email={fd.email}, "
            f"Maturity={fd.maturity_date}, "
            f"Days Left={days_left}"
        )

        if days_left in [30, 15, 7, 1, 0]:

            print(f"Sending email to {fd.email}")

            try:
                send_mail(
                    subject="FD Maturity Reminder",
                    message=f"Dear {fd.customer_name}, your FD {fd.fd_number} matures in {days_left} day(s).",
                    from_email="varuntalwai2020@gmail.com",
                    recipient_list=[fd.email],
                    fail_silently=False,
                )

                print(f"SUCCESS: Email sent to {fd.email}")

            except Exception as e:
                print(f"FAILED: {e}")