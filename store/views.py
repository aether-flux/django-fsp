import requests
from django.shortcuts import redirect, render
from django.http import FileResponse, Http404, HttpResponse
from django.conf import settings
from .models import *
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

def test(request):
    return HttpResponse('testing the page')

def test2(request):
    return HttpResponse('testing the second page')

def index(request):
    if 'aec' in request.session:
        u = request.session['aec']
        return render(request, 'index.html', { 'u': u })
    
    return render(request, 'index.html', { 'u': None })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def add(request):
    return render(request, 'add.html')

def evenodd(request):
    return render(request, 'evenodd.html')

def fibo(request):
    return render(request, 'fibonacci.html')

def calculator(request):
    return render(request, 'calculator.html')

def userInsertPage(request):
    return render(request, 'userInsert.html')


def sum(request):
    a = int(request.GET['a1'])
    b = int(request.GET['a2'])
    c = a + b

    return render(request, 'add.html', { 'a': c })

def evencheck(request):
    n = int(request.GET['n'])
    res = True

    if n % 2 != 0:
        res = False

    return render(request, 'evenodd.html', { 'res': res })

def fiboCalc(request):
    n = int(request.GET['n'])
    a = 0
    b = 1
    series = [a, b]

    for i in range(n-2):
        c = a+b
        series.append(c)
        a = b
        b = c

    return render(request, 'fibonacci.html', { 'series': series })

def calculate(request):
    a = int(request.GET['a'])
    b = int(request.GET['b'])
    # op = request.GET['operation']
    res = 0

    # if op == "Add":
    #     res = a + b
    # elif op == "Subtract":
    #     res = a - b
    # elif op == "Multiply":
    #     res = a * b
    # elif op == "Divide":
    #     if b == 0:
    #         res = -1
    #     else:
    #         res = a / b

    if 'add' in request.GET:
        res = a + b
    elif 'sub' in request.GET:
        res = a - b
    elif 'mul' in request.GET:
        res = a * b
    elif 'div' in request.GET:
        if b == 0:
            res = -1
        else:
            res = a / b

    return render(request, 'calculator.html', { 'res': res })

def ins(request):
    u = user()
    u.name = request.GET['name']
    u.email = request.GET['email']
    u.pwd = request.GET['pwd']
    u.phno = request.GET['phno']
    u.save()

    return render(request, 'userInsert.html')

def registerUser(request):
    s = student()
    s.firstname = request.GET['firstname']
    s.lastname = request.GET['lastname']
    s.address = request.GET['address']
    s.pincode = request.GET['pincode']
    s.city = request.GET['city']
    s.state = request.GET['state']
    s.fathername = request.GET['fathername']
    s.mothername = request.GET['mothername']
    s.phno = request.GET['phno']
    s.email = request.GET['email']
    s.aadharno = request.GET['aadhar']
    s.age = request.GET['age']
    s.save()

    return redirect('/store/register')

def show(request):
    u = user.objects.all()
    return render(request, 'show.html', { 'u': u })

def dele(request, id):
    u = user.objects.get(id=id)
    u.delete()
    return redirect('/store/show')

def edit(request, id):
    u = user.objects.get(id=id)
    return render(request, 'edit.html', { 'u': u })

def upd(request, id):
    u = user.objects.get(id=id)
    u.name = request.GET['name']
    u.email = request.GET['email']
    u.phno = request.GET['phno']
    u.save()

    return redirect('/store/show')

def loginProc(request):
    email = request.GET['email']
    pwd = request.GET['pwd']

    if 'aec' in request.session:
        return redirect('/store/login')

    u = user.objects.filter(email=email, pwd=pwd)
    # if not u:
    #     return redirect('/store/err?msg=loginerr')
    # if len(u) > 1:
    #     return redirect('/store/err?msg=multipleuserfound')
    # if not u or len(u) > 1:
    #     return redirect('/store/login')

    # u = user.objects.get(email=email, pwd=pwd)
    # if not u:
    #     return redirect('/err?msg="loginerr"')

    if u:
        u = u.first()
        x = { 'name': u.name, 'email': u.email }
        request.session['aec'] = x
        # return render(request, 'index.html')
        return redirect('/store/index')

    # return render(request, 'login.html')
    return redirect('/store/login')

def logout(request):
    del request.session['aec']
    return redirect('/store/index')

def fileupload(request):
    return render(request, 'upload.html')

def handle_upload(file, filename):
    if not os.path.exists('store/static/upload/'):
        os.mkdir('store/static/upload/')
    with open('store/static/upload/'+filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def upload(request):
    filename = str(request.FILES['a2'])
    allowed = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'heic', 'tiff', 'pdf']
    ext = filename.split('.')[-1]
    if ext not in allowed:
        return render(request, 'upload.html', { 'err': True })
    handle_upload(request.FILES['a2'], filename)
    url = "upload/" + str(request.FILES['a2'])
    u = picfile()
    u.fname = request.POST['a1']
    u.furl = url
    u.fext = ext
    u.save()
    return render(request, 'upload.html', { 'img': u })

def showimgs(request):
    imgs = picfile.objects.all()
    return render(request, 'showimgs.html', { 'imgs': imgs })

def download(request, id):
    f = picfile.objects.get(id=id)
    # filepath = os.path.join(str(settings.STATIC_ROOT), f.furl.url)
    filepath = str(settings.STATIC_ROOT) + f.furl.url
    if os.path.exists(filepath):
        with open(filepath, 'rb') as file:
            response = HttpResponse(file.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = "inline; filename=" + f.fname + "." + f.fext
            return response
    raise Http404

def weather_view(request):
    city = request.GET.get('city', 'Delhi')
    api_key = "40c8c5aaafd25bc0c9afa33872d2d40a"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    weather_data = {
        'city': data['name'],
        'country': data['sys']['country'],
        'temperature': data['main']['temp'],
        'main': data['weather'][0]['main'],
        'description': data['weather'][0]['description'],
        'windspeed': data['wind']['speed'],
        'humidity': data['main']['humidity'],
        'visibility': data['visibility'],
        'clouds': data['clouds'],
        'coord': data['coord'],
        'feels_like': data['main']['feels_like'],
        'mint': data['main']['temp_min'],
        'maxt': data['main']['temp_max'],
        'sea_level': data['main']['sea_level'],
        'grnd_level': data['main']['grnd_level'],
    }

    return render(request, 'weather.html', weather_data)



class ReactView(APIView):
    serializer_class = ReactSerializer

    def get(self, request):
        detail = [{ 'name': detail.name, 'email': detail.email, 'phno': detail.phno } for detail in user.objects.all()]
        return Response(detail)

    def post(self, request):
        serializer = ReactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
