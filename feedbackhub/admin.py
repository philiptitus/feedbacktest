from django.contrib import admin
from .models import CustomUser, Company, Category, Feedback, Notification,Metrics

admin.site.register(CustomUser)
admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Feedback)
admin.site.register(Notification)
admin.site.register(Metrics)
