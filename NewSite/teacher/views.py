from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from teacher import models
from .models import User,Teacher

#表单
class UserForm(forms.Form):
    #workID = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class UserForm2(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=100)
    status = forms.IntegerField()

class PwdForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

#登陆
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username=username, password= password)
            if user:
                for i in user:
                    status = i.status
                if status == 0:
                #比较成功，跳转index
                    response = HttpResponseRedirect('/dean/')
                #将username写入浏览器cookie,失效时间为3600
                    response.set_cookie('username',username,3600)
                    return response
                else :
                    response = HttpResponseRedirect('/faculty/')
                    response.set_cookie('username', username, 3600)
                    return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    #return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))
    return render(req, "login.html", {"uf":uf})

#教务处主页
def dean(request):
    username = request.COOKIES.get('username','')
    return render_to_response('dean.html' ,{'username':username})

#教务处教师列表
def teachertables(request):
    user_list = models.Teacher.objects.all()
    return render(request, "teachertables.html", {"data": user_list})

#教务处修改教师资料
def edit(request, teacher):
    teacher_ID = int(teacher)
    date = models.Teacher.objects.get(work_ID=teacher_ID)
    user = models.User.objects.get(username=teacher_ID)
    college_list = list(date.COL_CHOICES)
    title_list = list(date.TIT_CHOICES)
    edu_list = list(date.EDU_CHOICES)
    if request.method == 'POST':
        card_ID = request.POST['card_ID']
        sex = request.POST['sex']
        age = request.POST['age']
        email = request.POST['email']
        address = request.POST['address']
        entry_time = request.POST['entry_time']
        college = request.POST['college']
        phonenum = request.POST['phone']
        nation = request.POST['nation']
        birthplace = request.POST['birthplace']
        title = request.POST['title']
        firstedu = request.POST['firstedu']
        firstsch = request.POST['firstsch']
        finaledu = request.POST['finaledu']
        finalsch = request.POST['finalsch']
        check = request.POST['check']
        status = request.POST['status']
        honor= request.POST['honor']
        #input_img = request.FILES['input_img']
        models.Teacher.objects.filter(work_ID=teacher_ID).update(card_ID = card_ID, sex = sex, age = age,
                                                                 email = email, address = address, entry_time = entry_time,
                                                                 college = college, phonenum = phonenum, nation = nation,
                                                                 birthplace = birthplace, firstedu = firstedu,
                                                                 firstsch = firstsch, finaledu = finaledu, finalsch = finalsch,
                                                                 checkstatus = check, honor = honor,
                                                                 )
        models.User.objects.filter(username=teacher_ID).update(status = status)
        #models.Photo.objects.filter(username=teacher_ID).update(img = input_img)
        response = HttpResponseRedirect('/teachertables/')
        return response

    return render(request, "edit.html", {"data": date, "user":user, "college_list":college_list, "title_list":title_list, "edu_list":edu_list})
    #return HttpResponse('success!!')

#教务处删除教师
def delete(request, teacher):
    teacher_ID = int(teacher)
    data = models.User.objects.get(username=teacher_ID)
    if request.method == 'POST':
        models.Teacher.objects.get(work_ID=teacher_ID).delete()
        response = HttpResponseRedirect('/teachertables/')
        return response
    return render(request, "Delete.html",{"data":data})

#教务处查看教师资料
def check(request, teacher):
    teacher_ID = int(teacher)
    user_data = models.User.objects.get(username=teacher_ID)
    teacher_data = models.Teacher.objects.get(work_ID=teacher_ID)
    if request.method == 'POST':
        checkstatus = request.POST['check']
        models.Teacher.objects.filter(work_ID=teacher_ID).update(checkstatus = checkstatus)
        response = HttpResponseRedirect('/teachertables/')
        return response
    return render(request, "Check.html",{"user_data":user_data,"teacher_data":teacher_data})

#教务处新增教师
def teacherform(req):
    if req.method == 'POST':
        uf2 = UserForm2(req.POST)
        if uf2.is_valid():
            #获得表单数据
            User_QSet = User.objects.all()
            User_list = []
            for i in User_QSet:
                User_list = i
            last_ID = User_list.username_id
            work_ID = last_ID + 1
            username = uf2.cleaned_data['username']
            password = uf2.cleaned_data['password']
            status = uf2.cleaned_data['status']
            #添加到数据库
            Teacher.objects.create(work_ID=work_ID, name=username, entry_time='1980-01-01')
            NewUser = Teacher.objects.get(work_ID=work_ID)
            User.objects.create(username= NewUser,password=password,status=status)
            response = HttpResponseRedirect('/teachertables/')
            return response
    else:
        uf2 = UserForm()
    return render(req, "teacherform.html", {"uf2":uf2})

#评级
def rate(request, teacher):
    teacher_ID = int(teacher)
    user_data = models.User.objects.get(username=teacher_ID)
    teacher_data = models.Teacher.objects.get(work_ID=teacher_ID)
    if request.method == 'POST':
        year = request.POST['year']
        rate = request.POST['rate']
        divisor = int(year)
        ave = 0
        if divisor == 1:
            ave = models.Teacher.objects.get(work_ID=teacher_ID).last1
        if divisor == 2:
            ave = (models.Teacher.objects.get(work_ID=teacher_ID).last1 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last2)/2
        if divisor == 3:
            ave = (models.Teacher.objects.get(work_ID=teacher_ID).last1 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last2 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last3)/3
        if divisor == 4:
            ave = (models.Teacher.objects.get(work_ID=teacher_ID).last1 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last2 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last3 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last4)/4
        if divisor == 5:
            ave = (models.Teacher.objects.get(work_ID=teacher_ID).last1 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last2 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last3 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last4 +
                    models.Teacher.objects.get(work_ID=teacher_ID).last5)/5

        if ave >= 144:
            title = int(rate) - 1
        else:
            title = 3
        models.Teacher.objects.filter(work_ID=teacher_ID).update(rate = rate, title = title)
        response = HttpResponseRedirect('/teachertables/')
        return response
    return render(request, "rate.html",{"user_data":user_data,"teacher_data":teacher_data})


#教师主页
def faculty(request):
    username = request.COOKIES.get('username','')
    teacher_ID = int(username)
    teacher = models.Teacher.objects.get(work_ID=teacher_ID)
    user = models.User.objects.get(username=teacher_ID)
    return render_to_response('faculty.html' ,{'teacher_data':teacher,'user':user})

#教师基本信息
def BasinInf(request):
    username = request.COOKIES.get('username', '')
    teacher_ID = int(username)
    teacher = models.Teacher.objects.get(work_ID=teacher_ID)
    user = models.User.objects.get(username=teacher_ID)
    return render_to_response('BasicInf.html', {'teacher_data': teacher,'user':user})

def teacheredit(request):
    username = request.COOKIES.get('username', '')
    teacher_ID = int(username)
    teacher = models.Teacher.objects.get(work_ID=teacher_ID)
    user = models.User.objects.get(username=teacher_ID)
    college_list = list(teacher.COL_CHOICES)
    title_list = list(teacher.TIT_CHOICES)
    edu_list = list(teacher.EDU_CHOICES)
    if request.method == 'POST':
        card_ID = request.POST['card_ID']
        sex = request.POST['sex']
        age = request.POST['age']
        email = request.POST['email']
        address = request.POST['address']
        entry_time = request.POST['entry_time']
        college = request.POST['college']
        phonenum = request.POST['phone']
        nation = request.POST['nation']
        birthplace = request.POST['birthplace']
        title = request.POST['title']
        firstedu = request.POST['firstedu']
        firstsch = request.POST['firstsch']
        finaledu = request.POST['finaledu']
        finalsch = request.POST['finalsch']
        honor = request.POST['honor']
        models.Teacher.objects.filter(work_ID=teacher_ID).update(card_ID = card_ID, sex = sex, age = age,
                                                                 email = email, address = address, entry_time = entry_time,
                                                                 college = college, phonenum = phonenum, nation = nation,
                                                                 birthplace = birthplace, firstedu = firstedu,
                                                                 firstsch = firstsch, finaledu = finaledu, finalsch = finalsch,
                                                                 honor = honor, checkstatus = 0, )
        response = HttpResponseRedirect('/faculty/')
        return response
    return render_to_response('teacheredit.html', {'data': teacher,'user':user, "college_list":college_list, "title_list":title_list, "edu_list":edu_list})

def Addclasshour(request):
    username = request.COOKIES.get('username', '')
    teacher_ID = int(username)
    teacher = models.Teacher.objects.get(work_ID=teacher_ID)
    user = models.User.objects.get(username=teacher_ID)
    if request.method == 'POST':
        last5 = request.POST['last5']
        last4 = request.POST['last4']
        last3 = request.POST['last3']
        last2 = request.POST['last2']
        last1 = request.POST['last1']
        models.Teacher.objects.filter(work_ID=teacher_ID).update(last1 = last1, last2 = last2, last3 = last3,
                                                                 last4 = last4, last5 = last5, rate = 4,)
        response = HttpResponseRedirect('/faculty/')
        return response
    return render_to_response('addclasshour.html', {'teacher_data': teacher,'user':user})

#修改密码
def ChangePwd(request):
    username = request.COOKIES.get('username','')
    teacher_ID = int(username)
    user = models.User.objects.get(username=teacher_ID)
    if request.method == 'POST':
        pwd = PwdForm(request.POST)
        if pwd.is_valid():
            password = pwd.cleaned_data['password']
            models.User.objects.filter(username_id=teacher_ID).update(password = password)
            print(password)
            if models.User.objects.get(username_id=teacher_ID).status == 0:
                return render(request,"dean.html")
            else:
                return render(request,"faculty.html")
    return render_to_response('ChangePwd.html')


