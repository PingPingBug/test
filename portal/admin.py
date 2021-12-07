from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Students)
admin.site.register(models.Teacher)
admin.site.register(models.Attendence)
admin.site.register(models.Subject)
admin.site.register(models.Lecture)
admin.site.register(models.Department)
