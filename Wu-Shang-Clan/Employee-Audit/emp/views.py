from .models import AuditLog  # Import the AuditLog model or your equivalent
from copy import deepcopy
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .models import Employee, Task, AuditLog, Department, Project, Skill, Office, ProjectAssignment, EmployeeSkill, EmployeeOfficeAssignment, Position
from django.http import HttpResponse
from auditlog.models import LogEntry
from auditlog.registry import auditlog
from django.contrib.contenttypes.models import ContentType
from django.urls import path
from . import views


from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from .models import Employee, Task, AuditLog, Department, Project, Skill, Office, ProjectAssignment, EmployeeSkill, EmployeeOfficeAssignment, Position
from django.http import HttpResponse
from auditlog.models import LogEntry
from auditlog.registry import auditlog
from django.contrib.contenttypes.models import ContentType
from django.urls import path
from . import views
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DepartmentForm
from .forms import EmployeeSkillForm
from .forms import TaskForm
from django.core.exceptions import ObjectDoesNotExist


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                # Attempt to get the Employee based on the employee_id
                employee_id = form.cleaned_data['employee_id']
                employee = Employee.objects.get(id=employee_id)

                # Associate the task with the employee
                task = form.save(commit=False)
                task.employee = employee
                task.save()
                return redirect('task_list')
            except ObjectDoesNotExist:
                # Handle the case where the employee doesn't exist
                form.add_error(
                    'employee_id', 'Selected employee does not exist')
        # Handle the case where the form is not valid
    else:
        form = TaskForm()
    return render(request, 'emp/add_task.html', {'form': form})


def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'emp/task_list.html', {'tasks': tasks})


def emp_home(request):
    employees = Employee.objects.all()
    return render(request, "emp/home.html", {'emps': employees})


# def add_employee(request):
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


# def delete_employee(request, emp_id):
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
        # employees = Employee.object.all()
        # return render(request, "emp/home.html", {'employees': employees})
        # return redirect("emp_home")
        return redirect("http://127.0.0.1:8000/emp/home/")

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
    return redirect("http://127.0.0.1:8000/emp/home/")


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
        emp_department_name = request.POST.get(
            "emp_department")  # Get department name

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

        if emp_working is None:
            e.working = False
        else:
            e.working = True

        try:
            # Attempt to get the Department instance by name, and handle the case of multiple results
            department = Department.objects.get(name=emp_department_name)
        except Department.MultipleObjectsReturned:
            # Handle the case where multiple departments have the same name (you can choose the appropriate department)
            department = Department.objects.filter(
                name=emp_department_name).first()
        except Department.DoesNotExist:
            # Handle the case where no department with that name exists
            department = None

        e.department = department

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

        # return redirect("task_list")

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
    # return redirect("task_list")


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

        # return redirect("skill_list")

    return render(request, "emp/add_skill.html", {})


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
    return render(request, "emp/office_list.html", {'offices': offices})


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

        # return redirect("office_list")

    return render(request, "emp/add_office.html", {})


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
    # return redirect("office_list")


def project_assignment_list(request):
    project_assignments = ProjectAssignment.objects.all()
    return render(request, "emp/project_assignment_list.html", {'project_assignments': project_assignments})


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

        # return redirect("project_assignment_list")

    projects = Project.objects.all()
    employees = Employee.objects.all()
    return render(request, "emp/add_project_assignment.html", {'projects': projects, 'employees': employees})


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
    # return redirect("project_assignment_list")


def employee_skill_list(request):
    employee_skills = EmployeeSkill.objects.all()
    return render(request, "emp/employee_skill_list.html", {'employee_skills': employee_skills})


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

        # return redirect("employee_skill_list")

    employees = Employee.objects.all()
    skills = Skill.objects.all()
    return render(request, "emp/add_employee_skill.html", {'employees': employees, 'skills': skills})


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
    # return redirect("employee_skill_list")


def employee_office_assignment_list(request):
    employee_office_assignments = EmployeeOfficeAssignment.objects.all()
    return render(request, "emp/employee_office_assignment_list.html", {'employee_office_assignments': employee_office_assignments})


def add_employee_office_assignment(request):
    if request.method == "POST":
        employee_id = request.POST.get("employee_id")
        office_id = request.POST.get("office_id")

        # You should validate inputs, but for simplicity, we'll assume valid input here.

        employee_office_assignment = EmployeeOfficeAssignment(
            employee_id=employee_id, office_id=office_id)
        employee_office_assignment.save()

        # Log the creation of the employee office assignment
        log_entry = AuditLog(
            action='CREATE',
            model='EmployeeOfficeAssignment',
            object_id=employee_office_assignment.id,
            details=f'Employee assigned to office'
        )
        log_entry.save()

        return redirect("employee_office_assignment_list")

    employees = Employee.objects.all()
    offices = Office.objects.all()
    return render(request, "emp/add_employee_office_assignment.html", {'employees': employees, 'offices': offices})


def delete_employee_office_assignment(request, assignment_id):
    try:
        assignment = EmployeeOfficeAssignment.objects.get(pk=assignment_id)
        assignment.delete()
        # Redirect to the employee office assignment list after deletion
        return redirect('employee_office_assignment_list')
    except EmployeeOfficeAssignment.DoesNotExist:
        # Handle the case when the assignment doesn't exist
        # You can display an error message or perform other actions as needed
        pass


def update_employee_office_assignment(request, assignment_id):
    try:
        assignment = EmployeeOfficeAssignment.objects.get(pk=assignment_id)
    except EmployeeOfficeAssignment.DoesNotExist:
        # Handle the case when the assignment doesn't exist
        # You can display an error message or perform other actions as needed
        pass

    if request.method == 'POST':
        form = EmployeeOfficeAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('employee_office_assignment_list')
    else:
        form = EmployeeOfficeAssignmentForm(instance=assignment)

    return render(request, 'emp/update_employee_office_assignment.html', {'form': form, 'assignment': assignment})


def position_list(request):
    positions = Position.objects.all()
    return render(request, "emp/position_list.html", {'positions': positions})


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

        # return redirect("position_list")

    return render(request, "emp/add_position.html", {})


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
    # return redirect("position_list")


def add_department(request):
    if request.method == "POST":
        name = request.POST.get("department_name")  # Match the field name
        description = request.POST.get(
            "department_description")  # Match the field name

        department = Department(name=name, description=description)
        department.save()

        # Log the creation of the department
        log_entry = AuditLog(
            action='CREATE',
            model='Department',
            object_id=department.id,
            details=f'Department {department.name} created.'
        )
        log_entry.save()

        # Redirect to the department list view
        return redirect("department_list")

    return render(request, "emp/add_department.html", {})


def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == "POST":
        department.delete()
        # You can add an audit log entry for department deletion here if needed
        return redirect("department_list")  # Redirect to the department list

    # Handle GET request by rendering a confirmation page
    return render(request, "emp/confirm_department_delete.html", {"department": department})


def update_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)

    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            # You can add an audit log entry for department update here if needed
            # Redirect to the department list
            return redirect("department_list")

    else:
        form = DepartmentForm(instance=department)

    return render(request, "emp/update_department.html", {"form": form, "department": department})


def department_list(request):
    departments = Department.objects.all()
    return render(request, "emp/department_list.html", {'departments': departments})


# def get_audit_log_changes(model_instance, version_number):
#     # Get the audit log entries for the model instance
#     log_entries = LogEntry.objects.filter(
#         object_id=str(model_instance.id),
#         content_type_id=ContentType.objects.get_for_model(model_instance).id
#     ).order_by('timestamp')

#     try:
#         # Retrieve the LogEntry for the desired version
#         log_entry = log_entries[version_number - 1]
#         # Extract and return the changes as a dictionary
#         changes = log_entry.changes_dict
#         return changes
#     except IndexError:
#         return None


# model_instance = Employee.objects.get(pk=1)  # Get the model instance
# version_number = 3  # The desired version number

# changes = get_audit_log_changes(model_instance, version_number)
# if changes:
#     # Access the changes in the form of a dictionary
#     for key, (from_value, to_value) in changes.items():
#         print(f"Field: {key}, From: {from_value}, To: {to_value}")
# else:
#     print("Version not found or does not exist.")


# views.py


def initialize_object_with_audit_log(original_entity, end_change):
    # Clone the original entity to create an empty object.
    empty_object = Employee()

    # Get the audit log history for the original entity.
    audit_log = original_entity.history_dep.all().order_by('id')

    # Iterate over the changes from the audit log and apply them.
    for log_entry in audit_log[:end_change]:
        for field_name, (from_value, to_value) in log_entry.changes_dict.items():
            setattr(empty_object, field_name, to_value)

    return empty_object


# Replace with the correct primary key of the 'Department'.
original_entity_id = 5
end_change = 2  # User-specified end change

original_entity = Department.objects.get(pk=original_entity_id)
resulting_entity = initialize_object_with_audit_log(
    original_entity, end_change)


def display_entity(request, department_id, end_change):
    department = Department.objects.get(pk=department_id)

    # Get the department's audit log entries and filter them by department
    audit_log_entries = LogEntry.objects.filter(
        object_id=department_id,
        content_type_id=ContentType.objects.get_for_model(department).id
    ).order_by('id')

    # Create a list to store the changes
    changes = []

    for log_entry in audit_log_entries[:end_change]:
        change_dict = {}
        for field_name, (from_value, to_value) in log_entry.changes_dict.items():
            change_dict[field_name] = (from_value, to_value)
        changes.append(change_dict)  # Append the change dictionary to the list

    context = {
        'department': department,
        'changes': changes,
    }

    return render(request, 'emp/display_entity.html', context)


# def display_audit_log_changes(request, object_id):
#     # Get the audit log entries for the specified object ID, ordered by timestamp
#     audit_log_entries = AuditLog.objects.filter(
#         object_id=object_id).order_by('timestamp')

#     # You can change 'object_id' to match the field name you use in your AuditLog model

#     context = {
#         'audit_log_entries': audit_log_entries,
#     }

#     return render(request, 'emp/display_audit_log_changes.html', context)


def capture_audit_log(object_id, endpoint):
    # Get the audit log entries for the specified object, ordered by timestamp
    audit_log_entries = AuditLog.objects.filter(
        object_id=object_id).order_by('timestamp')

    # Slice the list to include only the entries up to the desired endpoint
    captured_entries = audit_log_entries[:endpoint]

    return captured_entries


def display_audit_log_changes(request, object_id, endpoint):
    # Call the utility function to capture audit log entries
    captured_entries = capture_audit_log(object_id, endpoint)

    context = {
        'captured_entries': captured_entries,
    }

    return render(request, 'emp/display_audit_log_changes.html', context)
