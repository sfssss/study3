from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .models import BoardMember
from .forms import LoginForm

def Loginsuccess(request):
    user_id = request.session.get('user')
    
    if user_id:
        member = BoardMember.objects.get(pk=user_id)
        return HttpResponse(member.username)

    return HttpResponse('Home!')
    
def login(request):
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')

    return render(request, 'login.html', {'form' : form})

def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')

def register(request):
    if request.method == "GET":
        return render(request, 'register.html')

    elif request.method == "POST":
        #print (request.POST)
        name    = request.POST.get('username', None)
        #print(username)
        password    = request.POST.get('password', None)
        #print(password)
        re_password = request.POST.get('re_password', None)
        #print(re_password)
        email       = request.POST.get('email', None)


        res_data = {}
        if not (name and password and re_password and email):
            res_data['error'] = '모든 값을 입력하세요!'

        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다'
            print(res_data)

        elif BoardMember.objects.filter(username=name).exists():
            res_data['error'] = '중복된 아이디입니다'

        else:
            member = BoardMember(
                username    = name,
                email       = email,
                password    = make_password(password)
            )
            member.save()
            return redirect('/')

        return render(request,'register.html', res_data)

