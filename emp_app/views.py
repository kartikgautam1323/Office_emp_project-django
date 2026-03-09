from django.shortcuts import render,redirect , HttpResponse
from django.contrib import messages
from.models import Employee,Role,Department
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request,'index.html') 


def all_emp(request):
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    print(context)
    return render(request,'all_emp.html',context) 


def add_emp(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login required to add employee")
        return redirect('/')
    dep = Department.objects.all()
    rol = Role.objects.all()

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone')

        dept_id = request.POST.get('dept')
        role_id = request.POST.get('role')

        department = Department.objects.get(id=dept_id)
        role = Role.objects.get(id=role_id)

        emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            dept=department,
            role=role,
            hire_date=datetime.now()
        )
        emp.save()
        messages.success(
                    request,
                    f"Employee {emp.first_name} {emp.last_name} added successfully!"
                )
        

        # After saving, redirect to view all employees
        return redirect('/')

    context = {
        'dep': dep,
        'rol': rol
    }
    return render(request, 'add_emp.html', context)




def remove_emp(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login required to add employee")
        return redirect('/')
    emps=Employee.objects.all()
    context={
        'emps':emps
    }
    if request.method == "POST":
        emp_id = request.POST.get('emp_id')

        if emp_id:
            try:
                emp = Employee.objects.get(id=emp_id)
                emp.delete()
                messages.success(
                    request,
                    f"Employee {emp.first_name} {emp.last_name} deleted successfully!"
                )
            except Employee.DoesNotExist:
                messages.error(request, "Employee not found.")
                  # optional: handle error message

        return redirect('remove_emp') 
    return render(request,'remove_emp.html',context) 






def filter_emp(request):
    dep=Department.objects.all()
    rol=Role.objects.all()

    if request.method=='POST':
        name=request.POST.get('name')
        dept=request.POST.get('dept')
        role=request.POST.get('role')
        emps=Employee.objects.all()
        if name:
            emps=emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps=emps.filter(dept__name=dept)
        if role:
            emps=emps.filter(role__name=role)
        context={
        'dep':dep,
        'rol':rol,
        'emps':emps
        }

        return render(request,'all_emp.html',context)
    elif request.method == 'GET':
        context={
        'dep':dep,
        'rol':rol,
        }
        return render(request,'filter_emp.html',context) 
    else:
        context={
        'dep':dep,
        'rol':rol,
        }
        return render(request,'filter_emp.html',context)
    

def handlesignup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        #1️⃣ Password match check
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("/")

        # 2️⃣ Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("/")

        # 3️⃣ Email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("/")

        # 4️⃣ Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully. You can login now.")

        return redirect("/")

    else:
        return HttpResponse('error')
    

def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user=authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'Successfully logged In')
            return redirect('/')
        else:
            messages.error("Invalid Credentials")
            return redirect('/')
    else:
        return HttpResponse('error')


def handlelogout(request):
    logout(request)
    messages.success(request,'Successfully logged Out')
    return redirect('/')

    