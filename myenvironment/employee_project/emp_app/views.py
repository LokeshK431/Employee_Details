from django.shortcuts import render, HttpResponse
from . models import Employee, Project, Department
from datetime import datetime
from django.db.models import Q


def index(request):
    return render(request, 'index.html')

def view_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'view_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept_id = request.POST['dept']
        project_id = request.POST['project']

        #Check if employee with same name already exists
        try:
            existing_emp = Employee.objects.get(name=name)
            return HttpResponse('Employee with same name alraedy exists')
        except Employee.DoesNotExist:
            pass

        #Retrieve department object from database.
        try:
            dept_obj = Department.objects.get(id=dept_id)

        except Department.DoesNotExist:
            return HttpResponse("Invalid Department")
        
        #Retrieve project object from database
        try:
            project_obj = Project.objects.get(id=project_id)

        except Project.DoesNotExist:
            return HttpResponse("Invaild Project")

        #Creating new employee object with department & project assigned
        new_emp = Employee(name=name, dept=dept_obj, project=project_obj)

        #Save new employee object to the database
        new_emp.save()

        return HttpResponse('Employee added successfully')
        
    elif request.method == 'GET':
        depts = Department.objects.all()
        projects = Project.objects.all()
        context = {
            'depts': depts,
            'projects': projects,
        }

        return render(request, 'add_emp.html',context)    
    else:
        
        return HttpResponse("Exception occured! Employee not added")

def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed!")
        except:
            return HttpResponse("Enter a Valid ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        project = request.POST['project']
        emps = Employee.objects.all()

        if name:
            emps = emps.filter(Q(name__icontains = name))
        if dept:
            emps = emps.filter(Q(dept__name__icontains = dept))
        if project:
            emps = emps.filter(Q(project__name__icontains = project))

        context = {
            'emps': emps
        }
        
        return render(request, 'view_emp.html', context)
    
    elif request.method == 'GET':

        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('Error occured!')