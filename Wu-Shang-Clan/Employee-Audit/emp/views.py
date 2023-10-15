from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Emp
from .models import CRUDLog


def emp_home(request):
    emps = Emp.objects.all()
    return render(request, "emp/home.html", {'emps': emps})


def add_emp(request):
    if request.method == "POST":
        emp_name = request.POST.get("emp_name")
        emp_id = request.POST.get("emp_id")
        emp_phone = request.POST.get("emp_phone")
        emp_address = request.POST.get("emp_address")
        emp_working = request.POST.get("emp_working")
        emp_department = request.POST.get("emp_department")
        e = Emp()
        e.name = emp_name
        e.emp_id = emp_id
        e.phone = emp_phone
        e.address = emp_address
        e.department = emp_department
        if emp_working is None:
            e.working = False
        else:
            e.working = True
        e.save()
        log_entry = CRUDLog(
            action='CREATE',
            model='Employee',
            object_id=e.id,  # The ID of the newly created employee
            details=f'Employee {e.name} created.'
        )
        log_entry.save()
        return redirect("/emp/home/")
    return render(request, "emp/add_emp.html", {})


def delete_emp(request, emp_id):
    emp = Emp.objects.get(pk=emp_id)
    log_entry = CRUDLog(
        action='DELETE',
        model='Employee',
        object_id=emp.id,  # The ID of the deleted employee
        details=f'Employee {emp.name} deleted.'
    )
    log_entry.save()
    emp.delete()
    return redirect("/emp/home/")


def update_emp(request, emp_id):
    emp = Emp.objects.get(pk=emp_id)
    print("Yes Bhai")
    return render(request, "emp/update_emp.html", {
        'emp': emp
    })


def do_update_emp(request, emp_id):
    if request.method == "POST":
        emp_name = request.POST.get("emp_name")
        emp_id_temp = request.POST.get("emp_id")
        emp_phone = request.POST.get("emp_phone")
        emp_address = request.POST.get("emp_address")
        emp_working = request.POST.get("emp_working")
        emp_department = request.POST.get("emp_department")

        e = Emp.objects.get(pk=emp_id)

        log_entry = CRUDLog(
            action='UPDATE',
            model='Employee',
            object_id=e.id,  # The ID of the updated employee
            details=f'Employee {e.name} updated.'
        )
        log_entry.save()

        e.name = emp_name
        e.emp_id = emp_id_temp
        e.phone = emp_phone
        e.address = emp_address
        e.department = emp_department
        if emp_working is None:
            e.working = False
        else:
            e.working = True
        e.save()
    return redirect("/emp/home/")


def view_logs(request):
    logs = CRUDLog.objects.all()
    return render(request, "emp/logs.html", {'logs': logs})
