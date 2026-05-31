from django.shortcuts import render, redirect, get_object_or_404
from .models import FD
from .forms import FDForm
from datetime import date, timedelta
from django.db.models import Avg
from django.http import HttpResponse
from openpyxl import Workbook
from django.core.mail import send_mail


def dashboard(request):

    search = request.GET.get('search', '')
    sort = request.GET.get('sort', '')

    fds = FD.objects.all()

    if search:
        fds = (
            FD.objects.filter(customer_name__icontains=search)
            |
            FD.objects.filter(bank_name__icontains=search)
        ).distinct()

    if sort == "earliest":
        fds = fds.order_by('maturity_date')
    else:
        fds = fds.order_by('-id')

    total_amount = 0
    total_maturity = 0

    for fd in fds:
        fd.days_left = (fd.maturity_date - date.today()).days

        total_amount += float(fd.amount)
        total_maturity += fd.maturity_amount()

    return render(
        request,
        "dashboard.html",
        {
            "fds": fds,
            "total_amount": round(total_amount, 2),
            "total_maturity": round(total_maturity, 2),
            "search": search,
            "sort": sort,
        }
    )


def mis_report(request):

    fds = FD.objects.all()

    total_fds = fds.count()

    total_investment = sum(
        float(fd.amount) for fd in fds
    )

    total_maturity = sum(
        fd.maturity_amount() for fd in fds
    )

    interest_earned = (
        total_maturity - total_investment
    )

    matured = fds.filter(
        maturity_date__lt=date.today()
    ).count()

    upcoming = fds.filter(
        maturity_date__gte=date.today(),
        maturity_date__lte=date.today() + timedelta(days=30)
    ).count()

    avg_interest = fds.aggregate(
        Avg('interest_rate')
    )['interest_rate__avg']

    return render(
        request,
        "mis_report.html",
        {
            "total_fds": total_fds,
            "total_investment": round(total_investment, 2),
            "total_maturity": round(total_maturity, 2),
            "interest_earned": round(interest_earned, 2),
            "matured": matured,
            "upcoming": upcoming,
            "avg_interest": round(avg_interest or 0, 2),
        }
    )


def add_fd(request):

    if request.method == "POST":
        form = FDForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = FDForm()

    return render(
        request,
        "add_fd.html",
        {"form": form}
    )


def edit_fd(request, id):

    fd = get_object_or_404(FD, id=id)

    if request.method == "POST":
        form = FDForm(
            request.POST,
            instance=fd
        )

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = FDForm(instance=fd)

    return render(
        request,
        "add_fd.html",
        {"form": form}
    )


def delete_fd(request, id):

    fd = get_object_or_404(FD, id=id)

    fd.delete()

    return redirect('/')
def export_excel(request):

    wb = Workbook()
    ws = wb.active

    ws.title = "FD Report"

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = (
        "attachment; filename=FD_Report.xlsx"
    )

    wb.save(response)

    return response
def test_email(request):
    try:
        send_mail(
            "FD Test Email",
            "If you received this email, SMTP is working.",
            "varuntalwai2020@gmail.com",
            ["varuntalwai2020@gmail.com"],
             fail_silently=False,
        )
        return HttpResponse("Mail Sent Successfully")
    except Exception as e:
        return HttpResponse(f"Mail Error: {e}")
             