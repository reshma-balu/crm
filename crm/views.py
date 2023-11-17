from django.shortcuts import render,redirect
from django.views.generic import View
# Create your views here.

from crm.forms import EmployeeForm,EmployeeModelForm,RegistrationForm,LoginForm
from crm.models import Employees
from crm.forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


class HomeView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"home.html")
    
    def post(self,request,*args,**kwargs):
        name=request.POST.get("boxs")
        qs=Employee.objects.filter(name_icontains=name)
        return render(request,"emplist.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EmployeeModelForm()
        return render(request,"emp_add.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=EmployeeModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"employee has been created")
            print("created")
            return render(request,"emp_add.html",{"form":form})
        else:
            messages.error(request,"failed to create employee")
            return render(request,"emp_add.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        # if request.user.is_authenticated:
        qs=Employees.objects.all()
        departments=Employees.objects.all().values_list("department",flat=True).distinct()
        print(departments)
        # print(request.GET)#department:"hr"
        # dep=request.GET.get("department")
        # qs=qs.filter(department=dep)
        if "department" in request.GET:
            dept=request.GET.get("department")
            qs=qs.filter(department__iexact=dept)
        return render(request,"emp_list.html",{"data":qs,"departments":departments})
        # else:
        #     messages.error(request,"invalid session")
        #     return redirect("signin")

    def post(self,request,*args,**kwargs):
        name=request.POST.get("box")
        qs=Employee.objects.filter(name=name)
        return render(request,"emp_list.html",{"data":qs})

@method_decorator(signin_required,name="dispatch")
#url:location:8000/employees/{pk}
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render(request,"emp_detail.html",{"data":qs})
@method_decorator(signin_required,name="dispatch")
class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        messages.success(request,"employee removed")
        return redirect("emp-all")
@method_decorator(signin_required,name="dispatch")
class EmployeeUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(instance=obj)
        return render(request,"emp_edit.html",{"form":form})

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"employee changed")
            return redirect("emp-details",pk=id)
        else:
            messages.error(request,"failed to change employee")
            return render(request,"emp_edit.html",{"form":form})

#localhost:8000/signup/
#get
#post
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
        #user.objects.create(**form.cleaned_data)
            User.objects.create_user(**form.cleaned_data)
            print("Saved")
            messages.success(request,"account has been created")
            return render(request,"register.html",{"form":form})
        else:
            print("Failed")
            messages.error(request,"failed to create account")
            return render(request,"register.html",{"form":form})

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            print(request.user,"before")
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(u_name,pwd)
            user_obj=authenticate(request,username=u_name,password=pwd)
            if user_obj:
                print("valid credential")
                login(request,user_obj)
                print(request.user,"after")
                return redirect("emp-all")
        messages.error(request,"invalid credential")

        return render(request,"login.html",{"form":form})
@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
        





