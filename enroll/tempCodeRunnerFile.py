def save_data(request):
    if request.method =="POST":
        form = StudentRegistration(request.POST)
        if form.is_valid():
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            usr = User(name=name,email=email,password=password)#create a object with parameter
            usr.save();
            stud = User.objects.values()#in the qurey set (like a json format)
            student_data = list(stud);
            print(stud)
            #returning the data on succes function in ajax
            return JsonResponse({'status':'Save','student_data':student_data})
        else:
            return JsonResponse({'status':0})
# ,'student_data':student_data