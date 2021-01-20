from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.login,name='login'),
    path('home/',views.home,name='home'),
    path('income/',views.IncomeView.as_view(),name="income"),
    path('income/type/',views.incometype,name='income-type'),
    path('expense/',views.ExpenseView.as_view(),name="expense"),
    path('expense/type/',views.expensetype,name='expense-type'),
    path('employee/',views.EmployeeView.as_view(),name='employee'),

    path('add/income/<str:incomemode>/',views.AddincomeView.as_view(),name ='add-income'),
    path('add/income-type/',views.AddIncomeTypeView.as_view(),name ='add-income-type'),
    path('add/expense/<str:expensemode>/',views.AddexpenseView.as_view(),name ='add-expense'),
    path('add/expense-type/',views.AddExpenseTypeView.as_view(),name='add-expense-type'),
    path('add/employee/',views.AddEmployeView.as_view(),name='add-employee'),

    path('income/<int:pk>/update/', views.IncomeUpdateView.as_view(), name='income-update'),
    path('expense/<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expense-update'),

    path("delete/income/<str:pk>/",views.IncomeDeleteView.as_view(),name='delete-income'),
    path("delete/expense/<str:pk>/",views.ExpenseDeleteView.as_view(),name='delete-expense'),
    
    path('report/',views.report,name='report'),

    path('opening/',views.AddOpeningView.as_view(),name="opening"),
    path('opening/details/',views.OpeningView.as_view(),name='open-details'),
    path('opening/<int:pk>/update/', views.OpeningUpdateView.as_view(), name='opening-update'),
    path('opening/<int:pk>/delete/', views.OpeningDeleteView.as_view(), name='delete-opening'),

    path('income-filter/',views.Incomefilter,name='income-filter'),
    path('expense-filter/',views.Expensefilter,name='expense-filter'),

    path('income-csv/',views.income_csv,name='income-csv'),
    path('expense-csv/',views.expense_csv,name='expense-csv'),

    path('recipt/<int:pk>/',views.ReciptView.as_view(),name="recipt"),
    path('test/<int:pk>/',views.TestView.as_view(),name='test'),

    path('register/',views.register,name='register'),
    path('logout/',views.logoutUser,name='logout'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_complete"),
]