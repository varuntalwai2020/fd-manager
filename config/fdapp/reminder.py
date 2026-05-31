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

        days_left = (fd.maturity_date - today).days

        print(
            f"Customer={fd.customer_name}, "
            f"Email={fd.email}, "
            f"Maturity={fd.maturity_date}, "
            f"Days Left={days_left}"
        )

        send_now = False

        if days_left == 30 and not fd.reminder_30_sent:
            send_now = True

        elif days_left == 15 and not fd.reminder_15_sent:
            send_now = True

        elif days_left == 7 and not fd.reminder_7_sent:
            send_now = True

        elif days_left == 1 and not fd.reminder_1_sent:
            send_now = True

        elif days_left == 0 and not fd.reminder_0_sent:
            send_now = True

        if send_now:

            print(f"Sending email to {fd.email}")

            try:
                send_mail(
                    subject="FD Maturity Reminder",
                    message=f"""
Dear {fd.customer_name},

Your Fixed Deposit details:

FD Number: {fd.fd_number}
Bank: {fd.bank_name}
Amount: ₹{fd.amount}

Your FD will mature in {days_left} day(s).

Regards,
FD Management System
""",
                    from_email="varuntalwai2020@gmail.com",
                    recipient_list=[fd.email],
                    fail_silently=False,
                )

                if days_left == 30:
                    fd.reminder_30_sent = True

                elif days_left == 15:
                    fd.reminder_15_sent = True

                elif days_left == 7:
                    fd.reminder_7_sent = True

                elif days_left == 1:
                    fd.reminder_1_sent = True

                elif days_left == 0:
                    fd.reminder_0_sent = True

                fd.save()

                print(f"SUCCESS: Email sent to {fd.email}")

            except Exception as e:
                print(f"FAILED: {e}")