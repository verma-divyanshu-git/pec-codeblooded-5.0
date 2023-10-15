from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .models import Employee, Task, AuditLog, Department, Project, Skill, Office, ProjectAssignment, EmployeeSkill, EmployeeOfficeAssignment, Position
from django.http import HttpResponse


def emp_home(request):
    employees = Employee.objects.all()
    return render(request, "emp/home.html", {'employees': employees})


# def add_employee(request):
#     if request.method == "POST":
#         emp_name = request.POST.get("emp_name")
#         emp_id = request.POST.get("emp_id")
#         emp_phone = request.POST.get("emp_phone")
#         emp_address = request.POST.get("emp_address")
#         emp_working = request.POST.get("emp_working")
#         emp_department_id = request.POST.get("emp_department")
#         emp_position_id = request.POST.get("emp_position")

#         # Check if the department ID exists
#         try:
#             department = Department.objects.get(id=emp_department_id)
#         except Department.DoesNotExist:
#             department = None

#         position = Position.objects.get(
#             id=emp_position_id) if emp_position_id else None

#         employee = Employee(name=emp_name, emp_id=emp_id, phone=emp_phone, address=emp_address,
#                             working=emp_working, department=department, position=position)
#         employee.save()

#         # Log the creation of the employee
#         log_entry = AuditLog(
#             action='CREATE',
#             model='Employee',
#             object_id=employee.id,
#             details=f'Employee {employee.name} created.'
#         )
#         log_entry.save()

#         return redirect("emp_home")

#     departments = Department.objects.all()
#     positions = Position.objects.all()
#     return render(request, "emp/add_employee.html", {'departments': departments, 'positions': positions})


def add_employee(request):
    if request.method == "POST":
        emp_name = request.POST.get("emp_name")
        emp_id = request.POST.get("emp_id")
        emp_phone = request.POST.get("emp_phone")
        emp_address = request.POST.get("emp_address")
        emp_working = request.POST.get("emp_working")
        emp_department_id = request.POST.get("emp_department")
        emp_position_id = request.POST.get("emp_position")

        emp_working = emp_working.lower() == 'true'

        department = Department.objects.get(
            id=1)
        position = Position.objects.get(
            id=emp_position_id) if emp_position_id else None

        employee = Employee(name=emp_name, emp_id=emp_id, phone=emp_phone, address=emp_address,
                            working=emp_working, department=department, position=position)
        employee.save()

        # Log the creation of the employee
        log_entry = AuditLog(
            action='CREATE',
            model='Employee',
            object_id=employee.id,
            details=f'Employee {employee.name} created.'
        )
        log_entry.save()

        # return redirect("emp_home")

    departments = Department.objects.all()
    positions = Position.objects.all()
    return render(request, "emp/add_employee.html", {'departments': departments, 'positions': positions})


def delete_employee(request, emp_id):
    employee = Employee.objects.get(pk=emp_id)

    # Log the deletion of the employee
    log_entry = AuditLog(
        action='DELETE',
        model='Employee',
        object_id=employee.id,
        details=f'Employee {employee.name} deleted.'
    )
    log_entry.save()

    employee.delete()
    return redirect("emp_home")


def update_emp(request, emp_id):
    emp = Employee.objects.get(pk=emp_id)
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

        e = Employee.objects.get(pk=emp_id)

        log_entry = AuditLog(
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
    # Sort logs by timestamp, most recent first
    logs = AuditLog.objects.all().order_by('-timestamp')
    page = request.GET.get('page')
    items_per_page = 10  # Number of log entries to display per page
    paginator = Paginator(logs, items_per_page)
    logs = paginator.get_page(page)
    return render(request, "emp/logs.html", {'logs': logs})


def task_list(request):
    tasks = Task.objects.all()
    return render(request, "emp/task_list.html", {'tasks': tasks})


def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        assigned_to_id = request.POST.get("assigned_to")
        due_date = request.POST.get("due_date")

        assigned_to = Employee.objects.get(id=assigned_to_id)

        task = Task(title=title, description=description,
                    assigned_to=assigned_to, due_date=due_date)
        task.save()

        # Log the creation of the task
        log_entry = AuditLog(
            action='CREATE',
            model='Task',
            object_id=task.id,
            details=f'Task {task.title} created.'
        )
        log_entry.save()

        return redirect("task_list")

    employees = Employee.objects.all()
    return render(request, "emp/add_task.html", {'employees': employees})


def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)

    # Log the deletion of the task
    log_entry = AuditLog(
        action='DELETE',
        model='Task',
        object_id=task.id,
        details=f'Task {task.title} deleted.'
    )
    log_entry.save()

    task.delete()
    return redirect("task_list")


def skill_list(request):
    skills = Skill.objects.all()
    return render(request, "emp/skill_list.html", {'skills': skills})


def add_skill(request):
    if request.method == "POST":
        skill_name = request.POST.get("skill_name")

        skill = Skill(name=skill_name)
        skill.save()

        # Log the creation of the skill
        log_entry = AuditLog(
            action='CREATE',
            model='Skill',
            object_id=skill.id,
            details=f'Skill {skill.name} created.'
        )
        log_entry.save()

        return redirect("skill_list")

    return render(request, "skill/add_skill.html", {})


def delete_skill(request, skill_id):
    skill = Skill.objects.get(pk=skill_id)

    # Log the deletion of the skill
    log_entry = AuditLog(
        action='DELETE',
        model='Skill',
        object_id=skill.id,
        details=f'Skill {skill.name} deleted.'
    )
    log_entry.save()

    skill.delete()
    return redirect("skill_list")


def office_list(request):
    offices = Office.objects.all()
    return render(request, "office/office_list.html", {'offices': offices})


def add_office(request):
    if request.method == "POST":
        office_name = request.POST.get("office_name")
        location = request.POST.get("location")

        office = Office(name=office_name, location=location)
        office.save()

        # Log the creation of the office
        log_entry = AuditLog(
            action='CREATE',
            model='Office',
            object_id=office.id,
            details=f'Office {office.name} created.'
        )
        log_entry.save()

        return redirect("office_list")

    return render(request, "office/add_office.html", {})


def delete_office(request, office_id):
    office = Office.objects.get(pk=office_id)

    # Log the deletion of the office
    log_entry = AuditLog(
        action='DELETE',
        model='Office',
        object_id=office.id,
        details=f'Office {office.name} deleted.'
    )
    log_entry.save()

    office.delete()
    return redirect("office_list")


def project_assignment_list(request):
    project_assignments = ProjectAssignment.objects.all()
    return render(request, "project_assignment/project_assignment_list.html", {'project_assignments': project_assignments})


def add_project_assignment(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        employee_id = request.POST.get("employee_id")

        project = Project.objects.get(id=project_id)
        employee = Employee.objects.get(id=employee_id)

        project_assignment = ProjectAssignment(
            project=project, employee=employee)
        project_assignment.save()

        # Log the creation of the project assignment
        log_entry = AuditLog(
            action='CREATE',
            model='ProjectAssignment',
            object_id=project_assignment.id,
            details=f'Project assignment created for {employee.name} on project {project.name}.'
        )
        log_entry.save()

        return redirect("project_assignment_list")

    projects = Project.objects.all()
    employees = Employee.objects.all()
    return render(request, "project_assignment/add_project_assignment.html", {'projects': projects, 'employees': employees})


def delete_project_assignment(request, project_assignment_id):
    project_assignment = ProjectAssignment.objects.get(
        pk=project_assignment_id)

    # Log the deletion of the project assignment
    log_entry = AuditLog(
        action='DELETE',
        model='ProjectAssignment',
        object_id=project_assignment.id,
        details=f'Project assignment deleted for {project_assignment.employee.name} on project {project_assignment.project.name}.'
    )
    log_entry.save()

    project_assignment.delete()
    return redirect("project_assignment_list")


def employee_skill_list(request):
    employee_skills = EmployeeSkill.objects.all()
    return render(request, "employee_skill/employee_skill_list.html", {'employee_skills': employee_skills})


def add_employee_skill(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        skill_id = request.POST.get("skill_id")

        employee = Employee.objects.get(id=employee_id)
        skill = Skill.objects.get(id=skill_id)

        employee_skill = EmployeeSkill(employee=employee, skill=skill)
        employee_skill.save()

        # Log the creation of the employee skill
        log_entry = AuditLog(
            action='CREATE',
            model='EmployeeSkill',
            object_id=employee_skill.id,
            details=f'Employee {employee.name} acquired skill {skill.name}.'
        )
        log_entry.save()

        return redirect("employee_skill_list")

    employees = Employee.objects.all()
    skills = Skill.objects.all()
    return render(request, "employee_skill/add_employee_skill.html", {'employees': employees, 'skills': skills})


def delete_employee_skill(request, employee_skill_id):
    employee_skill = EmployeeSkill.objects.get(pk=employee_skill_id)

    # Log the deletion of the employee skill
    log_entry = AuditLog(
        action='DELETE',
        model='EmployeeSkill',
        object_id=employee_skill.id,
        details=f'Employee {employee_skill.employee.name} lost skill {employee_skill.skill.name}.'
    )
    log_entry.save()

    employee_skill.delete()
    return redirect("employee_skill_list")


def employee_office_assignment_list(request):
    employee_office_assignments = EmployeeOfficeAssignment.objects.all()
    return render(request, "employee_office_assignment/employee_office_assignment_list.html", {'employee_office_assignments': employee_office_assignments})


def add_employee_office_assignment(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        office_id = request.POST.get("office_id")

        employee = Employee.objects.get(id=employee_id)
        office = Office.objects.get(id=office_id)

        employee_office_assignment = EmployeeOfficeAssignment(
            employee=employee, office=office)
        employee_office_assignment.save()

        # Log the creation of the employee office assignment
        log_entry = AuditLog(
            action='CREATE',
            model='EmployeeOfficeAssignment',
            object_id=employee_office_assignment.id,
            details=f'Employee {employee.name} assigned to office {office.name}.'
        )
        log_entry.save()

        return redirect("employee_office_assignment_list")

    employees = Employee.objects.all()
    offices = Office.objects.all()
    return render(request, "employee_office_assignment/add_employee_office_assignment.html", {'employees': employees, 'offices': offices})


def delete_employee_office_assignment(request, employee_office_assignment_id):
    employee_office_assignment = EmployeeOfficeAssignment.objects.get(
        pk=employee_office_assignment_id)

    # Log the deletion of the employee office assignment
    log_entry = AuditLog(
        action='DELETE',
        model='EmployeeOfficeAssignment',
        object_id=employee_office_assignment.id,
        details=f'Employee {employee_office_assignment.employee.name} removed from office {employee_office_assignment.office.name}.'
    )
    log_entry.save()

    employee_office_assignment.delete()
    return redirect("employee_office_assignment_list")


def position_list(request):
    positions = Position.objects.all()
    return render(request, "position/position_list.html", {'positions': positions})


def add_position(request):
    if request.method == "POST":
        position_name = request.POST.get("position_name")
        description = request.POST.get("description")

        position = Position(name=position_name, description=description)
        position.save()

        # Log the creation of the position
        log_entry = AuditLog(
            action='CREATE',
            model='Position',
            object_id=position.id,
            details=f'Position {position.name} created.'
        )
        log_entry.save()

        return redirect("position_list")

    return render(request, "position/add_position.html", {})


def delete_position(request, position_id):
    position = Position.objects.get(pk=position_id)

    # Log the deletion of the position
    log_entry = AuditLog(
        action='DELETE',
        model='Position',
        object_id=position.id,
        details=f'Position {position.name} deleted.'
    )
    log_entry.save()

    position.delete()
    return redirect("position_list")


def add_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        department = Department(
            name=name, description=description)
        department.save()

        # Log the creation of the department
        log_entry = AuditLog(
            action='CREATE',
            model='Department',
            object_id=department.id,
            details=f'Department {department.name} created.'
        )
        log_entry.save()

        # return redirect("department_list")

    return render(request, "emp/add_department.html", {})


def department_list(request):
    departments = Department.objects.all()
    return render(request, "emp/department_list.html", {'departments': departments})

