from django.shortcuts import redirect, render
from django.http import FileResponse, Http404, HttpResponse
from django.conf import settings
from .models import *
import os

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
    # filepath = os.path.join('store/static/', f.furl.url)
    # print(filepath)
    # if os.path.exists(filepath):
    #     print("file exists")
    #     with open(filepath, 'rb') as file:
    #         print("file opened")
    #         response = HttpResponse(file.read(), content_type="application/octet-stream")
    #         print("response created")
    #         response['Content-Disposition'] = "inline; filename=" + f.fname + "." + f.fext
    #         print("response header edited")
    #         return response
    # raise Http404

    # filepath = os.path.join(f.furl.url)
    filepath = settings.STATIC_ROOT
    print(filepath)

    if not os.path.exists(filepath):
        raise Http404

    response = FileResponse(open(filepath, 'rb'), as_attachment=True)
    response['Content-Disposition'] = (f'attachment; filename="{f.fname}/{f.fext}"')
    return response
