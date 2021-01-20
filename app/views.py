from django.shortcuts import get_object_or_404, redirect, render
from .models import(
    Expense,
    Income,
    IncomeType,
    ExpenseType,
    Employee,
    Opening
)
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.http import Http404
import csv
import datetime
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,logout,login as auth_login
from django.contrib.messages import success
from .forms import *
from num2words import num2words
# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        incomes = Income.objects.all()
        expenses = Expense.objects.all()
        total = 0 
        tot = 0
        for income in incomes:
            tot += income.incamt

        for expense in expenses:
            total += expense.amount

        context = {
            "tot":tot,
            "total":total
        }
        messages.success(request, "Logged in Successfully")
        return render(request,'index.html',context)
    else:
        return redirect('login')

class AddincomeView(LoginRequiredMixin,View):
    template_name = 'income-form.html'
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,incomemode):
        context={
            'incomemode':incomemode
        }
        return render(request,self.template_name,context)
    def post(self,request,incomemode):
        data = request.POST
        income = Income()
        income.incid = data['incid']
        income.incname =data['incname']
        income.incdate = data['incdate']
        income.incmode = data['incmode']
        income.incamt = data['incamt']
        income.increason = data['increason']
        income.incby = data['incby']
        income.bankname = data['bankname']
        income.chequeordd = data['chequeordd']
        income.dateinbank = data['dateinbank']
        income.save()
        return redirect("income")
        return render(request,self.template_name)

class IncomeView(LoginRequiredMixin,View):
    template_name = "income-details.html"
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,*args, **kwargs):
        incomes = Income.objects.all()
        total = 0
        for income in incomes:
            total += income.incamt

        context = { 
            "incomes":incomes,
            "total":total
        }
        return render(request,self.template_name ,context)

class IncomeUpdateView(LoginRequiredMixin,View):
    template_name = 'update-income.html'
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        income = get_object_or_404(Income,pk=pk)
        context = {
            'incname':income.incname,
            'incdate':income.incdate,
            'incmode':income.incmode,
            'incamt':income.incamt,
            'increason':income.increason,
            'incby':income.incby,
            'bankname':income.bankname,
            'chequeordd':income.chequeordd,
            'dateinbank':income.dateinbank,
        }
        return render(request,self.template_name,context)

    def post(self,request,pk):
        income = get_object_or_404(Income,pk=pk)
        data = request.POST
        income.incname = data['incname']
        income.incdate = data['incdate']
        income.incmode = data['incmode']
        income.incamt = data['incamt']
        income.increason = data['increason']
        income.incby = data['incby']
        income.bankname = data['bankname']
        income.chequeordd = data['chequeordd']
        income.dateinbank = data['dateinbank']
        income.save()
        return redirect('income')
        return render(request,self.template_name)

class IncomeDeleteView(LoginRequiredMixin,View):
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        income = Income.objects.get(pk=pk)
        income.delete()
        return redirect("income")

class AddIncomeTypeView(LoginRequiredMixin,View):
    template_name = 'income-type-form.html'
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        data = request.POST
        incometype = IncomeType()
        incometype.typeid = data['typeid']
        incometype.typename = data['typename']
        incometype.save()
        return redirect("income-type")
        return render(request,self.template_name)
        
@login_required
def incometype(request):
    context = {
        'incometypes':IncomeType.objects.all()
    }
    return render(request,'income-type-details.html',context)

class AddexpenseView(LoginRequiredMixin,View):
    template_name ="expense-form.html"
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,expensemode):
        context={
            'expensemode':expensemode
        }
        return render(request,self.template_name,context)
    def post(self,request,expensemode):
        data = request.POST
        expense = Expense()
        expense.expid = data['expid']
        expense.expname = data['expname']
        expense.expdate = data['expdate']
        expense.expmode = data['expmode']
        expense.amount = data['amount']
        expense.expreason = data['expreason']
        expense.expby = data['expby']
        expense.bankname = data['bankname']
        expense.chequeordd = data['chequeordd']
        expense.dateinbank = data['dateinbank']
        expense.detail = data['detail']
        expense.save()
        return redirect("expense")
        return render(request,self.template_name)

class ExpenseView(LoginRequiredMixin,View):
    template_name ="expense-details.html"
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request):
        expenses = Expense.objects.all()
        context = {
            "expenses":expenses
        }   
        return render(request,self.template_name ,context)

class ExpenseUpdateView(LoginRequiredMixin,View):
    template_name = 'update-expense.html'
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        expense = get_object_or_404(Expense,pk=pk)
        context = {
            'expname':expense.expname,
            'expdate':expense.expdate,
            'expmode':expense.expmode,
            'amount':expense.amount,
            'expreason':expense.expreason,
            'expby':expense.expby,
            'bankname':expense.bankname,
            'chequeordd':expense.chequeordd,
            'dateinbank':expense.dateinbank
        }
        return render(request,self.template_name,context)

    def post(self,request,pk):
        expense = get_object_or_404(Expense,pk=pk)
        data = request.POST
        expense.expname = data['expname']
        expense.expdate = data['expdate']
        expense.expmode = data['expmode']
        expense.amount = data['amount']
        expense.expreason = data['expreason']
        expense.expby = data['expby']
        expense.bankname = data['bankname']
        expense.chequeordd = data['chequeordd']
        expense.dateinbank = data['dateinbank']
        expense.detail = data['detail']
        expense.save()
        return redirect('expense')
        return render(request,self.template_name) 

class ExpenseDeleteView(LoginRequiredMixin,View):
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        expense = Expense.objects.get(pk=pk)
        expense.delete()
        return redirect("expense")

class EmployeeDeleteView(LoginRequiredMixin,View):
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        employe = Employee.objects.get(pk=pk)
        employe.delete()
        return redirect('employee')

class AddExpenseTypeView(LoginRequiredMixin,View):
    template_name = 'expense-type-form.html'
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        data = request.POST
        expensetype = ExpenseType()
        expensetype.etypeid = data['etypeid']
        expensetype.etypename = data['etypename']
        expensetype.save()
        return redirect("expense-type")
        return render(request,self.template_name)

@login_required
def expensetype(request):
    context = {
        'expensetypes':ExpenseType.objects.all()
    }
    return render(request,'expense-type-details.html',context)

class AddEmployeView(LoginRequiredMixin,View):
    template_name = 'employee-form.html'
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        data = request.POST
        employe = Employee()
        employe.empid = data['empid']
        employe.empname =data['empname']
        employe.desination = data['desination']
        employe.desginkdda = data['desginkdda']
        employe.phone = data['phone']
        employe.address = data['address']
        employe.save()
        return redirect("employee")
        return render(request,self.template_name)

class EmployeeView(LoginRequiredMixin,View):
    template_name ="employee-details.html"
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request):
        employees = Employee.objects.all()
        context = {
            "employees":employees
        }
        return render(request,self.template_name ,context)

class EmployeeUpdateView(LoginRequiredMixin,View):
    template_name = "update-employee.html"
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        employee = get_object_or_404(Employee,pk=pk)
        context = {
            'empname':employee.empname,
            'desination':employee.desination,
            'desginkdda':employee.desginkdda,
            'phone':employee.phone,
            'address':employee.address
        }
        return render(request,self.template_name,context)

    def post(self,request,pk):
        employee = get_object_or_404(Employee,pk=pk)
        data = request.POST
        employee.empname = data['empname']
        employee.desination = data['desination']
        employee.desginkdda = data['desginkdda']
        employee.phone = data['phone']
        employee.address = data['address']
        employee.save()
        return redirect('employee')
        return render(request,self.template_name)

class EmployeeDeleteView(LoginRequiredMixin,View):
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        employe = Employee.objects.get(pk=pk)
        employe.delete()
        return redirect('employee')

@login_required
def report(request):
    incomes = Income.objects.all()
    expenses = Expense.objects.all()
    openings = Opening.objects.all()

    tot = 0
    for income in incomes:
        tot += income.incamt

    amt = 0
    for opening in openings:
        amt = opening.cashinhand + opening.cashatbank
        #x = tot+opening.cashatbank
            
    fin = amt+tot
    '''
    extot = 0
    for expense in expenses:
            extot += expense.amount
            y = x-extot
         
        cih = fin-(extot+y)
        
        finexp =  cih+y+extot
    '''
    extot = 0
    a=0
    for expense in expenses:
        extot += expense.amount
        a=fin-extot

    b=0
    for opening in openings:
        b=a-opening.cashatbankexp

    finexp = extot+a
    date = datetime.date.today()

    result = Income.objects.values('incname').annotate(total_amt=Sum('incamt'))
    expx = Expense.objects.values('expname').annotate(exp_tot=Sum('amount'))

    context = {
        "result":result,
        "expx":expx,
        "tot":tot,#all income tot
        "extot":extot,# all exp tot or closing balance
        "openings":openings,
        "fin":fin,# final income
        #"y":y, cash at bank
        #"cih":cih, cash in hand
        #"finexp":finexp final expense 
        "b":b,
        "finexp":finexp,
        "date":date
    }
    return render(request,'report.html',context)

class AddOpeningView(LoginRequiredMixin,View):
    template_name = 'starting.html'
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        data = request.POST
        opening = Opening()
        opening.cashinhand = data['cashinhand']
        opening.cashatbank = data['cashatbank']
        opening.cashatbankexp = data['cashatbankexp']
        opening.save()
        return redirect('open-details')
        return render(request,self.template_name)

class OpeningView(LoginRequiredMixin,View):
    template_name ="starting-details.html"
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request):
        openings = Opening.objects.all()
        context = {
            "openings":openings
        }
        return render(request,self.template_name ,context)

class OpeningUpdateView(LoginRequiredMixin,View):
    template_name = 'opening-update.html'
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        opening = get_object_or_404(Opening,pk=pk)
        context = {
            'cashinhand':opening.cashinhand,
            'cashatbank':opening.cashatbank,
            'cashatbankexp':opening.cashatbankexp
        }
        return render(request,self.template_name,context)
    def post(self,request,pk):
        opening = get_object_or_404(Opening,pk=pk)
        data = request.POST
        opening.cashinhand = data['cashinhand']
        opening.cashatbank = data['cashatbank']
        opening.cashatbankexp = data['cashatbankexp']
        opening.save()
        return redirect('open-details')
        return render(request,self.template_name)

class OpeningDeleteView(LoginRequiredMixin,View):
    raise_exception = True
    permission_denied_message = 'You must Login Now.'
    def get(self,request,pk):
        opening = Opening.objects.get(pk=pk)
        opening.delete()
        return redirect('open-details')

@login_required
def Incomefilter(request):
    inc = Income.objects.filter(incdate__gte=datetime.date(2022,10,1),incdate__lte=datetime.date(2020,10,30)).all()
    con = {
        "incms":inc
    }
    if request.method == 'POST':
        maxi = request.POST.get('date_max').split('-')
        mini = request.POST.get('date_min').split('-')
        incm = Income.objects.filter(incdate__gte=datetime.date(int(mini[0]),int(mini[1]),int(mini[2])),incdate__lte=datetime.date(int(maxi[0]),int(maxi[1]),int(maxi[2]))).all()          
        con = {
            "incms":incm,
        }
    return render(request,'income-filter.html',con)

@login_required
def Expensefilter(request):
    exp = Expense.objects.filter(expdate__gte=datetime.date(2022,10,1),expdate__lte=datetime.date(2020,10,30)).all()
    con = {
        "expms":exp
    }
    if request.method == 'POST':
        maxi = request.POST.get('date_max').split('-')
        mini = request.POST.get('date_min').split('-')
        expm = Expense.objects.filter(expdate__gte=datetime.date(int(mini[0]),int(mini[1]),int(mini[2])),expdate__lte=datetime.date(int(maxi[0]),int(maxi[1]),int(maxi[2]))).all()          
        con = {
            "expms":expm,
        }
    return render(request,'expense-filter.html',con)

@login_required
def income_csv(request):
    incomes = Income.objects.all() 
    response = HttpResponse(content_type = 'text\csv')
    response['content-Disposition'] = 'attachement; filename="income.csv"'
    writer = csv.writer(response,delimiter=',')
    writer.writerow(['IncName','Incdate','Incmode','Incamt','Increason','Incby','BankName','Cheque(or)DD','Dateinbank'])
    for income in incomes:
        writer.writerow([income.incname,income.incdate,income.incmode,income.incamt,income.increason,income.incby,income.bankname,income.chequeordd,income.dateinbank])
    return response

@login_required
def expense_csv(request):
    expenses = Expense.objects.all() 
    response = HttpResponse(content_type = 'text\csv')
    response['content-Disposition'] = 'attachement; filename="expense.csv"'
    writer = csv.writer(response,delimiter=',')
    writer.writerow(['Expname','Expdate','Expmode','Amount','Expreason','Expby','Detail','BankName','Cheque(or)dd','Dateinbank'])
    for expense in expenses:
        writer.writerow([expense.expname,expense.expdate,expense.expmode,expense.amount,expense.expreason,expense.expby,expense.detail,expense.bankname,expense.chequeordd,expense.dateinbank])
    return response

def login(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				auth_login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')
		context = {}
		return render(request, 'accounts/login.html', context) 

def logoutUser(request):
    logout(request)
    return redirect('login')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            return redirect('login')
    context = {
        'form':form
    } 
    return render(request,'accounts/register.html',context)    
	    

class TestView(View):
    template_name = 'voucher.html'
    def get(self,request,pk):
        expense = get_object_or_404(Expense,pk=pk)
        b = num2words(expense.amount)
        context = {
            'expid':expense.expid,
            'expname':expense.expname,
            'expdate':expense.expdate,
            'expmode':expense.expmode,
            'amount':expense.amount,
            'expreason':expense.expreason,
            'expby':expense.expby,
            'b':b
        }
        return render(request,self.template_name,context)

    def post(self,request,pk):
        expense = get_object_or_404(Expense,pk=pk)
        data = request.POST
        expense.expid = data['expid']
        expense.expname = data['expname']
        expense.expdate = data['expdate']
        expense.expmode = data['expmode']
        expense.amount = data['amount']
        expense.expreason = data['expreason']
        expense.expby = data['expby']
        return render(request,self.template_name)

class ReciptView(View):
    template_name = 'recipt.html'
    def get(self,request,pk):
        income = get_object_or_404(Income,pk=pk)
        a = num2words(income.incamt)
        context = {
            'incid':income.incid,
            'incname':income.incname,
            'incdate':income.incdate,
            'incmode':income.incmode,
            'incamt':income.incamt,
            'incby':income.incby,
            'bankname':income.bankname,
            'chequeordd':income.chequeordd,
            'dateinbank':income.dateinbank,
            'a':a
        }
        return render(request,self.template_name,context)

    def post(self,request,pk):
        income = get_object_or_404(Income,pk=pk)
        data = request.POST
        income.incname = data['incname']
        income.incdate = data['incdate']
        income.incmode = data['incmode']
        income.incamt = data['incamt']
        income.incby = data['incby']
        income.bankname = data['bankname']
        income.chequeordd = data['chequeordd']
        income.dateinbank = data['dateinbank']
        return render(request,self.template_name)