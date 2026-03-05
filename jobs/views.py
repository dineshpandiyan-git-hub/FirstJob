from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import User, Job, Application
import PyPDF2

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/choose-role/')
        else:
            return render(request, "login.html", {
                "error": "Invalid username or password. Please register if you don’t have an account."
            })

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        if User.objects.filter(username=request.POST.get("username")).exists():
            return render(request, "register.html", {"error": "Username exists"})
        user = User.objects.create_user(
            username=request.POST.get("username"),
            email=request.POST.get("email"),
            password=request.POST.get("password")
        )
        login(request, user)
        return redirect('/choose-role/')
    return render(request, "register.html")

@login_required
def choose_role(request):
    return render(request, "choose_role.html")

@login_required
def recruiter_dashboard(request):
    if request.method == "POST":
        Job.objects.create(
            recruiter=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            required_skills=request.POST.get("skills")
        )
        return render(request, "confirmation.html")

    jobs = Job.objects.filter(recruiter=request.user)
    return render(request, "recruiter_dashboard.html", {"jobs": jobs})

@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, "job_list.html", {"jobs": jobs})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        resume = request.FILES.get("resume")
        reader = PyPDF2.PdfReader(resume)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        skills = job.required_skills.lower().split(',')
        match = sum(1 for skill in skills if skill.strip() in text.lower())
        score = (match / len(skills)) * 100 if skills else 0

        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=resume,
            match_score=score
        )

        return render(request, "match_result.html", {"score": score})

    return render(request, "apply.html", {"job": job})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def about_page(request):
    return render(request, "about.html")

@login_required
def view_applicants(request, job_id):
    job = Job.objects.get(id=job_id, recruiter=request.user)
    applications = Application.objects.filter(job=job)

    return render(request, "applicants.html", {
        "job": job,
        "applications": applications
    })

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    job.delete()
    return redirect('/recruiter/')

@login_required
def update_application_status(request, app_id, action):
    application = get_object_or_404(Application, id=app_id)

    if application.job.recruiter != request.user:
        return redirect('/recruiter/')

    if request.method == "POST":
        if action == "accept":
            application.status = "Accepted"
        elif action == "reject":
            application.status = "Rejected"

        application.save()

    return redirect(f'/applicants/{application.job.id}/')

@login_required
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user)

    return render(request, "my_applications.html", {
        "applications": applications
    })