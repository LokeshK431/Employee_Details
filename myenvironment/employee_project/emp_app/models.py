from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100,null=False)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Project(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100, null=False)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name