from django.db import models
# from datetime import datetime
from django.utils import timezone
from datetime import datetime
# Create your models here.

class Applicant(models.Model):
    name = models.CharField(max_length=15, default="First")
    email = models.EmailField(max_length=50, default="Email")
    contact = models.CharField(max_length=10, default="0123456789")
    password = models.CharField(max_length=250, default="Passwd")
    role = models.CharField(max_length=20, default="applicant")
    location = models.CharField(max_length=20, default="applicant")
    gender = models.CharField(max_length=20, default="applicant")
    totalPoints = models.IntegerField(default="50")
    date_of_creation = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created = timezone.now()
    #     # self.modified = timezone.now()
    #     return super(Applicant, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

class Company(models.Model):
    name = models.CharField(max_length=20, default="name")
    email = models.EmailField(max_length=50, default="email")
    password = models.CharField(max_length=250, default="passwd")
    role = models.CharField(max_length=20, default="company")
    is_active = models.BooleanField(default=False)
    date_of_creation = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created = timezone.now()
    #     # self.modified = timezone.now()
    #     return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email
    
class Grievance(models.Model):
    Usr = models.ForeignKey(Applicant, on_delete=models.SET_NULL, null=True)
    Company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    Name = models.CharField(max_length=45, default="")
    Date = models.DateTimeField(default=datetime.now())
    Description = models.TextField(default="")
    Status = models.CharField(max_length=20, default="Grievance Filled")
    Comments = models.TextField(default="")

class Jobapplication(models.Model):
    companyId = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=20, default="company")
    description = models.TextField(default="")
    location = models.CharField(max_length=50, default="")
    jobType = models.CharField(max_length=20, default="Remote")
    startDate = models.DateField(auto_now_add=False, default=datetime.now())
    duration = models.CharField(max_length=20, default="")
    stipend = models.CharField(max_length=10, default="")
    skillsRequired = models.TextField(default="")
    whoCanApply = models.TextField(default="")
    totalOpenings = models.IntegerField(default="")
    availableOpenings = models.IntegerField(default="")
    isInternship = models.BooleanField(default=False)
    jobUploadedOn = models.DateTimeField(default=datetime.now())

class Application(models.Model):
    userId = models.ForeignKey(Applicant, on_delete=models.SET_NULL, null=True)
    jobId = models.ForeignKey(Jobapplication, on_delete=models.SET_NULL, null=True)
    appliedOn = models.DateTimeField(default=datetime.now())
    isSelected = models.BooleanField(default=False)
    bidPoints = models.IntegerField(default="")
    answer = models.TextField(default="")
    applicationViewed = models.BooleanField(default=False)
    isClosed = models.BooleanField(default=False)
    chatExists = models.BooleanField(default=False)

class Chat(models.Model):
    userId = models.ForeignKey(Applicant, on_delete=models.SET_NULL, null=True)
    jobId = models.ForeignKey(Jobapplication, on_delete=models.SET_NULL, null=True)
    applicationId = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True)
    createdOn = models.DateTimeField(default=datetime.now())
    isActive = models.BooleanField(default=True)
    