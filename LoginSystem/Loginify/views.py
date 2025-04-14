from django.shortcuts import redirect, render

from django.http import HttpResponse, JsonResponse

from .models import UserDetails
import json
from django.views.decorators.csrf import csrf_exempt

# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if UserDetails.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        
        user = UserDetails(username=username, email=email, password=password)
        user.save()
        return redirect('login')
    return render(request, 'signup.html')

# Login view
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                return render(request, 'success.html', {'username': user.username})
            else:
                return render(request, 'login.html', {'error': 'Incorrect password'})
        except UserDetails.DoesNotExist:
            return render(request, 'login.html', {'error': 'User not found'})
        
    return render(request, 'login.html')

#get all useres method
@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = list(UserDetails.objects.values())
        return JsonResponse(users, safe=False)

#get by email
@csrf_exempt
def get_user_by_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        try:
            user = UserDetails.objects.get(email=email)
            return JsonResponse({
                'username': user.username,
                'email': user.email,
                'password': user.password
            })
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

#update operation
@csrf_exempt
def update_user(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            user = UserDetails.objects.get(email=email)
            user.password = data.get('password', user.password)
            user.save()

            return JsonResponse({'message': 'User updated successfully'})
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


#Delete operation
@csrf_exempt
def delete_user(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        email = data.get('email')
        try:
            user = UserDetails.objects.get(email=email)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except UserDetails.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
