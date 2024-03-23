from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json

def register(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@csrf_exempt
def user_page(request):

    if(request.method == 'POST'):
        filename = "attentiveness\\"
        filename += request.body.decode()
        print(filename)
        with open(filename) as file:
            lines = [line.rstrip() for line in file]
        res = {}
        for line in lines:
            x = line.split("-")
            if x[0] not in res:
                res[x[0]] = x[1]
            else:
                res[x[0]] = res[x[0]] + "," +str(x[1])
        json_object = json.dumps(res, indent = 4) 
        return HttpResponse(str(json_object))
    else:
        return render(request, 'users/user_page.html')

        
