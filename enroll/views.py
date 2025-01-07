from django.shortcuts import render
from .forms import StudentRegistration
from .models import User
from django.http import JsonResponse

def home(request):
    form = StudentRegistration()
    stud = User.objects.all()
    return render(request, 'enroll/home.html', {'form': form, 'stu': stud})

def save_data(request):
    if request.method == "POST":
        form = StudentRegistration(request.POST)
        if form.is_valid():
            # Retrieve the hidden 'id' field (stuid)
            student_id = request.POST.get('stuid')  # This is for editing an existing user
            
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # If an ID exists, we update the user, otherwise create a new user
            if student_id:
                try:
                    # Update existing user
                    usr = User.objects.get(id=student_id)
                    usr.name = name
                    usr.email = email
                    usr.password = password
                    usr.save()
                    status = 'Updated'
                except User.DoesNotExist:
                    return JsonResponse({'status': 0, 'message': 'User not found'})
            else:
                # Create new user if no ID is provided
                usr = User(name=name, email=email, password=password)
                usr.save()
                status = 'Saved'
            
            # Fetch all students after save or update
            stud = User.objects.values('id', 'name', 'email', 'password')
            student_data = list(stud)
            
            return JsonResponse({'status': status, 'student_data': student_data})
        else:
            return JsonResponse({'status': 0, 'message': 'Form is not valid'})

def delete_data(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        try:
            idtodel = User.objects.get(pk=id)
            idtodel.delete()
            return JsonResponse({'status': 1})
        except User.DoesNotExist:
            return JsonResponse({'status': 0, 'message': 'User not found'})
    else:
        return JsonResponse({'status': 0})

def edit_data(request):
    if request.method == "POST":
        student_id = request.POST.get('sid')
        try:
            student = User.objects.get(id=student_id)
            student_data = {
                "status": "success",
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "password": student.password
            }
            return JsonResponse(student_data)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Student not found"})