from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Employee)
admin.site.register(Expense)
admin.site.register(Income)
admin.site.register(IncomeType)
admin.site.register(ExpenseType)
admin.site.register(Opening)