from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.http import JsonResponse
from django.http import QueryDict
# from django.db.models import Count
# import imp
# from dateutil.relativedelta import relativedelta
# from datetime import datetime
# from dateutil import tz


def send_otp_email(otp, email):
    subject = "Verify your Email - {}".format(email)
    print(otp)
    message = "Your 4-digit OTP to verify your account is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def send_psw_email(otp, email):
    subject = "Reset your Password - {}".format(email)
    print(otp)
    message = "Your 4-digit OTP to reset your password is : " + str(otp) + ". Please don't share it with anyone else"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def Register(request):
    if request.method == "POST":
        fnd1 = Applicant.objects.filter(email = request.POST['email'].lower())
        fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) == 0 and len(fnd2) == 0:
            request.session['name'] = request.POST['name']
            request.session['email'] = request.POST['email'].lower()
            request.session['password'] = request.POST['password']
            request.session['role'] = request.POST['role']
            cpswd = request.POST['confirmPassword']

            if request.session['password'] == cpswd:
                if request.session['role'] == 'applicant':
                    request.session['contact'] = request.POST['contact']
                    request.session['location'] = request.POST['location']
                    request.session['gender'] = request.POST['gender']

                request.session['password'] = make_password(request.POST['password'])
                request.session['otp'] = random.randint(1000,9999)
                send_otp_email(request.session['otp'], request.session['email'])
                messages.success(request, "OTP is sent to your email. Please enter it.")
                return redirect("verifyotppage")
            else:
                messages.error(request, "Password and Confirm Password do not match. Please try again")
                return redirect("register")
        else:
            messages.error(request, "User already exists. Please login")
            return redirect("login")
    else:
        return render(request, "app/auth-register-applicant.html")

def Login(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        pswd = request.POST['password']
        fnd1 = Applicant.objects.filter(email = request.POST['email'].lower())
        fnd2 = Company.objects.filter(email = request.POST['email'].lower())
        if len(fnd1) > 0:
            if check_password(pswd, fnd1[0].password):
                request.session['id'] = fnd1[0].id
                request.session['name'] = fnd1[0].name
                request.session['email'] = fnd1[0].email
                request.session['role'] = fnd1[0].role
                request.session['totalPoints'] = fnd1[0].totalPoints
                return redirect("dashboard")
            else:
                messages.error(request, "Please enter a valid password")
                return redirect("login")
        elif len(fnd2) > 0:
            if fnd2[0].is_active == True:
                if check_password(pswd, fnd2[0].password):
                    request.session['id'] = fnd2[0].id
                    request.session['name'] = fnd2[0].name
                    request.session['email'] = fnd2[0].email
                    request.session['role'] = fnd2[0].role
                    return redirect("dashboard")
                else:
                    messages.error(request, "Please enter a valid password")
                    return redirect("login")
            else:
                messages.error(request, "Account locked. Contact admin to unlock.")
                return redirect("login")
        else:
            messages.error(request, "User does not exist. Please register.")
            return redirect("register")
    else:
        return render(request, "app/auth-login.html")
    
def Logout(request):
    if 'email' in request.session:
        if request.session['role'] == 'applicant':
            del request.session['totalPoints']
        del request.session['id']
        del request.session['name']
        del request.session['email']
        del request.session['role']
        return redirect("login")
    else:
        return redirect("login")

def VerifyOTPPage(request):
    return render(request, "app/auth-register-otp.html")

def FpEmailPage(request):
    return render(request, "app/auth-fp-email.html")

def FpOTPPage(request):
    return render(request, "app/auth-fp-otp.html")

def FpPasswordPage(request):
    return render(request, "app/auth-fp-password.html")

def VerifyOTP(request):
    if request.method == "POST":
        name = request.session['name']
        role = request.session['role']
        email = request.session['email']
        mainotp = request.POST['otp']
        print(type(mainotp), type(request.session['otp']))
        if request.session['otp'] == int(mainotp):
            if role == 'company':
                addCompany = Company.objects.create(
                    name = name,
                    email = email,
                    password = request.session['password']
                )
                del request.session['password']
                del request.session['email']
                del request.session['name']
                del request.session['otp']
                del request.session['role']
            else:
                contact = request.session['contact']
                gender = request.session['gender']
                location = request.session['location']
                applicant = Applicant.objects.create(
                    name = name,
                    email = email,
                    contact = contact,
                    location = location,
                    gender = gender,
                    password = request.session['password']
                )
                del request.session['password']
                del request.session['email']
                del request.session['name']
                del request.session['contact']
                del request.session['gender']
                del request.session['location']
                del request.session['otp']
                del request.session['role']
            messages.success(request, "You have Registered successfully. Login to continue.")
            return redirect("login")
        else:
            messages.error(request, "Invalid OTP. Please try again")
            return redirect("verifyotppage")

def FpEmail(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        user1 = Applicant.objects.filter(email = email)
        user2 = Company.objects.filter(email = email)
        if user1:
            request.session['email'] = email
            request.session['role'] = 'applicant'
            request.session['otp'] = random.randint(1000,9999)
            send_psw_email(request.session['otp'], request.session['email'])
            return redirect("fpotppage")
        if user2:
            request.session['email'] = email
            request.session['role'] = 'company'
            request.session['otp'] = random.randint(1000,9999)
            send_psw_email(request.session['otp'], request.session['email'])
            return redirect("fpotppage")
        else:
            messages.error(request, "User does not exist. Please Register")
            return redirect("register")

def FpOTP(request):
    if request.method == "POST":
        eml = request.session['email'].lower()
        mainotp = request.POST['otp']
        if request.session['otp'] == int(mainotp):
            del request.session['otp']
            return redirect("fppasswordpage")
        else:
            messages.error(request, "Invalid OTP. Please try again")
            return redirect("fpotppage")

def FpPassword(request):
    if request.method == "POST":
        if request.session['role'] == 'company':
            fnd = Company.objects.get(email = request.session['email'])
        else:
            fnd = Applicant.objects.get(email = request.session['email'])
        pswd = request.POST['password']
        cpswd = request.POST['confirmPassword']
        if pswd == cpswd:
            fnd.password = make_password(pswd)
            fnd.save()
            del request.session['email']
            del request.session['role']
            messages.success(request, "Password changed successfully. Login to continue.")
            return redirect("login")
        else:
            messages.error(request, "Password and Confirm Password do not match. Please try again")
            return redirect("fppasswordpage")

def CompanyRegister(request):
    return render(request, 'app/auth-register-company.html')



def Dashboard(request):
    if 'email' in request.session:
        
        # l18 = FIR.objects.filter(S_age = "<18").count()
        # b1824 = FIR.objects.filter(S_age = "18-24").count()
        # b2544 = FIR.objects.filter(S_age = "25-44").count()
        # b4564 = FIR.objects.filter(S_age = "45-64").count()
        # graph 2
        totalJobs = Jobapplication.objects.all().count()
        # print(totalJobs)
        totalCompanies = Company.objects.all().count()
        # print(totalCompanies)
        totalCandidates = Applicant.objects.all().count()
        # print(totalCandidates)
        # graph 3
        jobAccepted = Application.objects.filter(isSelected = True).count()
        jobRejected = Application.objects.filter(isSelected = False).count()
        appNotViewed = Application.objects.filter(applicationViewed = True).count()
        # graph 1
        today = date.today()
        today = Application.objects.filter(appliedOn__year=today.year, appliedOn__month=today.month, appliedOn__day=today.day).count()
        all = Application.objects.all().count()
        uptilNow = all-today

        if request.session['role'] == 'applicant':
            user = Applicant.objects.get(email = request.session['email'])
            myApplications = Application.objects.filter(userId = user).order_by('-id')[:3]
            jobs = Jobapplication.objects.all().order_by('-id')[:3]
            return render(request, 'app/dashboard-new.html', {
            'jobAccepted':jobAccepted,
            'jobRejected':jobRejected,
            'appNotViewed':appNotViewed,
            'today':today,
            'uptilNow':uptilNow,
            'totalJobs':totalJobs,
            'totalCompanies':totalCompanies,
            'totalCandidates':totalCandidates,
            'myApplications': myApplications, 
            'jobs': jobs,
        })

        return render(request, 'app/dashboard-new.html', {
            'jobAccepted':jobAccepted,
            'jobRejected':jobRejected,
            'appNotViewed':appNotViewed,
            'today':today,
            'uptilNow':uptilNow,
            'totalJobs':totalJobs,
            'totalCompanies':totalCompanies,
            'totalCandidates':totalCandidates,
        })
    else:
        messages.error(request, "Please login to view dashboard")
        return redirect("login")

def AddJobs(request):
    if 'email' in request.session:
        if request.method == "POST":
            companyId = Company.objects.get(email=request.session['email'])
            name = request.POST['name']
            description = request.POST['description']
            location = request.POST['location']
            jobType = request.POST['jobType']
            startDate = request.POST['startDate']
            duration = request.POST['duration']
            stipend = request.POST['stipend']
            skillsRequired = request.POST['skillsRequired']
            whoCanApply = request.POST['whoCanApply']
            totalOpenings = int(request.POST['totalOpenings'])
            availableOpenings = int(request.POST['availableOpenings'])
            isInternship = request.POST['isInternship']
            if isInternship == 'Yes':
                isInternship = True
            else:
                isInternship = False
            job = Jobapplication.objects.create(
                companyId=companyId,
                name=name,
                description = description,
                location = location,
                jobType = jobType,
                startDate = startDate,
                duration = duration,
                stipend = stipend,
                skillsRequired = skillsRequired,
                whoCanApply = whoCanApply,
                totalOpenings = totalOpenings,
                availableOpenings = availableOpenings,
                isInternship = isInternship,
            )
            job.save()
            return redirect("jobs")
        else:
            email = request.session['email']
            allJobs = Jobapplication.objects.filter(companyId__email = email)
            return render(request, 'app/add-jobs-new.html', {'jobs': allJobs})
    else:
        messages.error(request, "Please login to view jobs")
        return redirect("login")

def UpdateJobs(request, pk):
    if 'email' in request.session:
        try:
            report = Jobapplication.objects.get(id=pk)
        except:
            messages.error(request, "Job does not exist.")
            return redirect("jobs")
        if request.method == "POST":
            report.name = request.POST['name']
            report.description = request.POST['description']
            report.location = request.POST['location']
            report.jobType = request.POST['jobType']
            report.startDate = request.POST['startDate']
            report.duration = request.POST['duration']
            report.stipend = request.POST['stipend']
            report.skillsRequired = request.POST['skillsRequired']
            report.whoCanApply = request.POST['whoCanApply']
            report.totalOpenings = request.POST['totalOpenings']
            report.availableOpenings = request.POST['availableOpenings']
            isInternship = request.POST['isInternship']
            print('=====>', isInternship)
            if isInternship == "Yes":
                report.isInternship = True
            else:
                report.isInternship = False
            report.save()
            return redirect("jobs")
        else:
            data = {
                'name': report.name,
                'description': report.description,
                'location': report.location,
                'jobType': report.jobType,
                'startDate': report.startDate,
                'duration': report.duration,
                'skillsRequired': report.skillsRequired,
                'stipend': report.stipend,
                'whoCanApply': report.whoCanApply,
                'totalOpenings': report.totalOpenings,
                'availableOpenings': report.availableOpenings,
                'isInternship': report.isInternship,
                'jobUploadedOn': report.jobUploadedOn,
            }
            return JsonResponse({'data': data})
    else:
        messages.error(request, "Please login to view jobs")
        return redirect("login")

def JobDelete(request, pk):
    if 'email' in request.session:
        try:
            report = Jobapplication.objects.get(id=pk)
            report.delete()
            messages.success(request, "Job deleted successfully.")
            return redirect("jobs")
        except:
            messages.error(request, "Could not delete the Job. Please try again.")
            return redirect("jobs")
    else:
        return redirect("login")

def GrievancesAdmin(request):
    if request.method == "POST":
        print('------------')
        try:

            messages.success(request, 'We will get back to you in a while!')
            return redirect("dashboard")
        except:
            messages.error(request, 'Could not submit the form. Please try again.')
            return redirect("")
    else:
        grv = Grievance.objects.all()
        company = Company.objects.all()
        return render(request, 'app/grievance-admin-new.html', {"grv":grv, 'companies': company})



def GrievancesUser(request):
    if request.method == "POST":
        print('------------')
        try:
            user = Applicant.objects.get(email=request.session['email'])
            name = request.POST['name']
            description= request.POST['desc']
            company = request.POST['company']
            company = Company.objects.get(name=company)
            ans = Grievance.objects.create(
                Name = name,
                Description = description,
                Usr = user,
                Company = company,
            )
            messages.success(request, 'We will get back to you in a while!')
            return redirect("grievance-user")
        except:
            messages.error(request, 'Could not submit the form. Please try again.')
            return redirect("grievance-user")
        
    grv = Grievance.objects.filter(Usr__email = request.session['email'])
    company = Company.objects.all()
    print(grv)
    return render(request, 'app/grievance-user-new.html', {"grv":grv, 'companies': company})

def UpdateGrievance(request, pk):
    if 'email' in request.session:
        try:
            report = Grievance.objects.get(id=pk)
        except:
            messages.error(request, "Grievance does not exist.")
            return redirect("grievance")
        if request.method == "POST":
            company = request.POST['company']
            report.Company = Company.objects.get(name=company)
            report.Name = request.POST['title']
            report.Description = request.POST['description']
            report.Statuc = request.POST['status']
            report.Comments = request.POST['comments']
            report.save()
            return redirect("grievance-admin")
        else:
            data = {
                'name': report.Name,
                'company': report.Company.name,
                'description': report.Description,
                'status': report.Status,
                'comments': report.Comments,
            }
            return JsonResponse({'data': data})
    else:
        messages.error(request, "Please login to view grievances")
        return redirect("login")

def GrievanceDelete(request, pk):
    if 'email' in request.session:
        try:
            report = Grievance.objects.get(id=pk)
            report.delete()
            messages.success(request, "Job deleted successfully.")
            return redirect("jobs")
        except:
            messages.error(request, "Could not delete the Job. Please try again.")
            return redirect("jobs")
    else:
        return redirect("login")


def jobList(request):
    jobs = Jobapplication.objects.all()
    if request.method=="POST":
        user = Applicant.objects.get(email=request.session['email'])
        bidPoints = int(request.POST['bidPoints'])
        jobId = int(request.POST['jobId'])
        app = Application.objects.filter(userId=user, jobId=jobId)
        if len(app) >0:
            messages.error(request, 'You have already applied for this job. Please wait while the company is reviewing your application')
            return redirect("job-list")
        remainingPoints = user.totalPoints - bidPoints
        if remainingPoints < 0:
            messages.error(request, "You don't have enough bidding points")
            return redirect("job-list")
        user.totalPoints = remainingPoints
        request.session['totalPoints'] = remainingPoints
        user.save()
        jobId = Jobapplication.objects.get(id=jobId)
        application = Application.objects.create(
            bidPoints = bidPoints,
            userId = user,
            jobId = jobId
        )
        application.save()
        messages.success(request, 'Application filled successfully')
        return redirect("job-list")
    return render(request, "app/job-list-new.html", {"jobs":jobs})



def ViewApplications(request):
    if 'email' in request.session:
        company = Company.objects.get(email = request.session['email'])
        jobs = Jobapplication.objects.filter(companyId = company)
        applications = {}
        for job in jobs:
            temp = Application.objects.filter(jobId = job).values('id', 'userId__name', 'jobId__name', 'jobId__id', 'appliedOn', 'isSelected', 'bidPoints', 'chatExists')
            applications[temp] = job.name
        query_dict = QueryDict('', mutable=True)
        query_dict.update(applications)
        print(query_dict)
        return render(request, 'app/applications-company-new.html', {'applications': query_dict})

def ViewApplicationDetails(request, pk):
    if 'email' in request.session:
        application = Application.objects.get(id = pk)
        application.applicationViewed = True
        application.save()
        applicant = Applicant.objects.get(id = application.userId.id)
        data = {
            'id': applicant.id,
            'name': applicant.name,
            'email': applicant.email,
            'contact': applicant.contact,
            'location': applicant.location,
            'gender': applicant.gender,
            'bids': application.bidPoints,
            'answer': application.answer,
        }
        return JsonResponse({'data': data})
    
def ViewCompany(request):
    if 'email' in request.session:
        companies = Company.objects.all()
        return render(request, 'app/company-new.html', {'companies': companies})


def Samp(request):
    val = ""
    if request.method == "POST":
        print(request.body)
        val = request.body['description']
        print('---------------->', val)
        return redirect("samp")
    else:
        return render(request, 'app/rte.html', {'val': val})






def UpdatePoints(request):
    if 'email' in request.session:
        print('if')
        jobs = Jobapplication.objects.filter(availableOpenings = 0)
        for job in jobs:
            print(job, '\n\n')
            applications = Application.objects.filter(jobId=job, applicationViewed=False, isClosed=False)
            for application in applications:
                print(application, '\n')
                user = Applicant.objects.get(id = application.userId.id)
                user.totalPoints = user.totalPoints + application.bidPoints
                application.isClosed = True
                user.save()
                application.save()
        messages.success(request, 'Points updated successfully')
        return redirect("dashboard")


def AddCompany(request):
    if 'email' in request.session:
        email = request.session['email']
        companies = Company.objects.all()
        return render(request, 'app/company-new.html', {'companies': companies})
    else:
        messages.error(request, "Please login to view companies")
        return redirect("login")

def UpdateCompany(request, pk):
    if 'email' in request.session:
        try:
            report = Company.objects.get(id=pk)
        except:
            messages.error(request, "Company does not exist.")
            return redirect("companies")
        if request.method == "POST":
            is_active = request.POST['isActive']
            if is_active == "Yes":
                report.is_active = True
            else:
                report.is_active = False
            report.save()
            return redirect("companies")
        else:
            count = Grievance.objects.filter(Company = report).count()
            data = {
                'name': report.name,
                'email': report.email,
                'is_active': report.is_active,
                'date_of_creation': report.date_of_creation,
                'isInternship': report.isInternship,
                'jobUploadedOn': report.jobUploadedOn,
                'count': count,
            }
            return JsonResponse({'data': data})
    else:
        messages.error(request, "Please login to view companies")
        return redirect("login")

def UpdateCompanyStatus(request, pk):
    if 'email' in request.session:
        try:
            company = Company.objects.get(id=pk)
        except:
            messages.error(request, "Company does not exist.")
            return redirect("companies")
        if request.method == "POST":
            is_active = request.POST['status']
            if is_active == "True":
                company.is_active = True
            else:
                company.is_active = False
            company.save()
            return redirect("companies")
        else:
            count = Grievance.objects.filter(Company = company).count()
            data = {
                'name': company.name,
                'email': company.email,
                'is_active': company.is_active,
                'date_of_creation': company.date_of_creation,
                'count': count,
            }
            return JsonResponse({'data': data})
    else:
        messages.error(request, "Please login to view companies")
        return redirect("login")


def CompanyDelete(request, pk):
    if 'email' in request.session:
        try:
            report = Company.objects.get(id=pk)
            report.delete()
            messages.success(request, "Company deleted successfully.")
            return redirect("company")
        except:
            messages.error(request, "Could not delete the company. Please try again.")
            return redirect("company")
    else:
        return redirect("login")

def StartChat(request):
    if 'email' in request.session:
        if request.method == 'POST':
            print(request.POST)
            userId = request.POST['userId']
            jobId = request.POST['jobId']
            applicationId = request.POST['applicationId']
            userId = Applicant.objects.get(id = userId)
            jobId = Jobapplication.objects.get(id = jobId)
            applicationId = Application.objects.get(id = applicationId)
            applicationId.chatExists = True
            applicationId.save()
            chat = Chat.objects.create(
                userId = userId,
                jobId = jobId,
                applicationId = applicationId,
            )
            return redirect("view-applications")
        else:
            if request.session['role'] == 'admin':
                chats = Chat.objects.all()
                return render(request, 'app/view-chats.html', {'chats': chats})
            if request.session['role'] == 'company':
                company = Company.objects.get(email = request.session['email'])
                jobs = Jobapplication.objects.filter(companyId = company)
                chats = {}
                for job in jobs:
                    temp = Chat.objects.filter(jobId = job).values('id', 'userId__name', 'jobId__name', 'applicationId__isSelected', 'createdOn', 'isActive')
                    chats[temp] = job.name
                query_dict = QueryDict('', mutable=True)
                query_dict.update(chats)
                print(query_dict)
                return render(request, 'app/view-chats.html', {'chats': query_dict})
            else:
                user = Applicant.objects.get(email = request.session['email'])
                chats = Chat.objects.filter(userId = user)
                return render(request, 'app/view-chats.html', {'chats': chats})
    else:
        messages.error(request, "Please login to view companies")
        return redirect("login")


def MyApplications(request):
    if 'email' in request.session:
        user = Applicant.objects.get(email = request.session['email'])
        applications = Application.objects.filter(userId = user)
        return render(request, 'app/applications-user.html', {'applications': applications})
    else:
        messages.error(request, "Please login to view applicants")
        return redirect("login")


def AllApplicants(request):
    if 'email' in request.session:
        applicants = Applicant.objects.all()
        return render(request, 'app/applicants.html', {'applicants': applicants})
    else:
        messages.error(request, "Please login to view applicants")
        return redirect("login")

def AdminUpdateApplicant(request, pk):
    if 'email' in request.session:
        try:
            report = Applicant.objects.get(id=pk)
        except:
            messages.error(request, "Applicant does not exist.")
            return redirect("dashboard")
        if request.method == "POST":
            report.name = request.POST['name']
            report.email = request.POST['email']
            report.contact = request.POST['contact']
            report.location = request.POST['location']
            report.gender = request.POST['gender']
            report.totalPoints = int(request.POST['totalPoints'])
            isActive = request.POST['isActive']
            if isActive == "Yes":
                report.isActive = True
            else:
                report.isActive = False
            report.save()
            return redirect("applicants")
        else:
            data = {
                'name': report.name,
                'email': report.email,
                'contact': report.contact,
                'location': report.location,
                'gender': report.gender,
                'totalPoints':report.totalPoints,
                'isActive':report.isActive,
            }
            return JsonResponse({'data': data})
    else:
        messages.error(request, "Please login to view applicants")
        return redirect("login")

def AdminDeleteApplicant(request, pk):
    if 'email' in request.session:
        try:
            report = Applicant.objects.get(id=pk)
            report.delete()
            messages.success(request, "Applicant deleted successfully.")
            return redirect("applicants")
        except:
            messages.error(request, "Could not delete the Applicant. Please try again.")
            return redirect("applicants")
    else:
        messages.error(request, "Please login to view applicants")
        return redirect("login")