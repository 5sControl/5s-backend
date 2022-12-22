from django.urls import path, include


routes = [
    path('employees/', include('apps.Employees.urls')),
]
