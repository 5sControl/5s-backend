from django.urls import path, include


routes = [
    path('employees/', include('apps.Employees.urls')),
    path('locations/', include('apps.Locations.urls')),
]
