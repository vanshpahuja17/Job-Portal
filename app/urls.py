from django.urls import path
from .views import *

urlpatterns = [
    path("register/", Register, name="register"),
    path("", Login, name="login"),
    path("logout/", Logout, name="logout"),

    path("otp-verification/", VerifyOTPPage, name="verifyotppage"),
    path("forgot-password-email/", FpEmailPage, name="fpemailpage"),
    path("forgot-password-otp/", FpOTPPage, name="fpotppage"),
    path("forgot-password-reset/", FpPasswordPage, name="fppasswordpage"),

    path("verify-otp/", VerifyOTP, name="verify-otp"),
    path("fp-email/", FpEmail, name="fp-email"),
    path("fp-otp/", FpOTP, name="fp-otp"),
    path("fp-password/", FpPassword, name="fp-password"),

    path('samp/', Samp, name="samp"),
    path('register-company/', CompanyRegister, name="register-company"),

    

    path('dashboard/', Dashboard, name="dashboard"),
    path('jobs/', AddJobs, name="jobs"),
    path('update-job/<int:pk>/', UpdateJobs, name="update-job"),
    path('delete-job/<int:pk>/', JobDelete, name="delete-job"),

    path("grievance-user/", GrievancesUser, name="grievance-user"),
    path("grievance-admin/", GrievancesAdmin, name="grievance-admin"),
    
path("job-list/", jobList, name="job-list"),
path("view-applications/", ViewApplications, name="view-applications"),
path("view-application-details/<int:pk>/", ViewApplicationDetails, name="view-application-details"),
path("update-points/", UpdatePoints, name="update-points"),
path("companies/", AddCompany, name="companies"),
path("update-company/<int:pk>/", UpdateCompany, name="update-company"),
path("update-company-status/<int:pk>/", UpdateCompanyStatus, name="update-company-status"),
path("delete-company/<int:pk>/", CompanyDelete, name="delete-company"),




path("chat/", StartChat, name="chat"),
    path("update-grievance/<int:pk>/", UpdateGrievance, name="update-grievance"),
    path("delete-grievance/<int:pk>/", GrievanceDelete, name="delete-grievance"),
    path("my-applications/", MyApplications, name="my-applications"),

    path("company/", ViewCompany, name="company"),
    path('update-applicant/<int:pk>/', AdminUpdateApplicant, name="update-applicant"),
    path('delete-applicant/<int:pk>/', AdminDeleteApplicant, name="delete-applicant"),
    path('applicants/', AllApplicants, name="applicants"),

]
