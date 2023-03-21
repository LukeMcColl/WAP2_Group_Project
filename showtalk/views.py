from django.shortcuts import render,HttpResponseRedirect
from showtalk.models import user,tv,pl
from django.http import HttpResponse

def homepage(request):
    if request.method == 'GET':
        get_page = request.GET.get("page")
        print(get_page)
        if get_page =="" or get_page==None:
            #pull videos
                tvall  =tv.objects.all
                return render(request, 'showtalk/index.html', locals())

        else:
            id = get_page
            tvall = tv.objects.get(id=id)
            # #pull commit
            plall = pl.objects.filter(tv_id = id)
            return render(request, 'showtalk/homepage.html', locals())


def register(request):
    if request.method == 'GET':
            return render(request,"login/register.html")



    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        password = request.POST.get('password')

        up_sql = user.objects.create(username=username,name=name,password=password)
        up_tv = tv.objects.create(user_id=up_sql.id,title="default video",docs="default info")
        return HttpResponse("register ok")
        # return HttpResponseRedirect('/')

def logout(request):
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    if "name" in request.session:
        del request.session["name"]
    resp = HttpResponseRedirect('/')
    return resp

def login(request):
    if request.method == 'GET':
        if request.session.get('username'):
            return HttpResponse('already logged in')

        else:
            return render(request,"login/login.html")



    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            test = user.objects.get(username=username,password=password)
            request.session['username'] = test.username
            request.session['uid'] = test.id

            request.session['name'] = test.name
        except:
            return HttpResponse("Account password error")


        return HttpResponseRedirect('/')


def profile(request):
    if request.method =="GET":

        try:
            uid = request.session.get("uid")
            userall = user.objects.filter(id=uid)
        except:
            return HttpResponseRedirect('/login')

        return render(request,'showtalk/profile.html',locals())

    if request.method =="POST":
        uid = request.session.get('uid')

        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get('email')
        bio = request.POST.get('bio')
        favourite = request.POST.get('favourite')
        img = request.FILES.get("img")

        #fix
        try:
            x = user.objects.get(id=uid)
            if name != '':
                x.name = name
            if username != '':
                x.username = username
            if password != "":
                x.password = password
            if favourite !="":
                x.favourite_shows = favourite
            if bio !="":
                x.bio = bio
            if email !="":
                x.email = email
            if img !="":
                x.img = img
            x.save() #done/save
            return HttpResponse("uplord successfully")
        except Exception as e:
            print(e)
            return HttpResponse("uplord fail")

def pinglun(request):
    if request.method =="POST":
        pinglun = request.POST.get('pinglun')
        uid = request.session.get('uid')
        tvid = request.POST.get('id')
        try:
            pl.objects.create(doc=pinglun,user_id=uid,tv_id=tvid)
            return HttpResponse("send successfully")

        except:
            return HttpResponse("send fail")

def tvv(request):
    if request.method == "GET":
        try:
            uid = request.session.get("uid")
            tvall = tv.objects.filter(user_id=uid)
        except:
            return HttpResponseRedirect('/login')

        return render(request, 'showtalk/tv.html', locals())

    if request.method == "POST":
        uid = request.session.get('uid')

        title = request.POST.get("title")
        docs= request.POST.get("docs")
        tvv = request.FILES.get("tv")

        # fix
        try:
            x = tv.objects.get(user_id=uid)
            if docs != "":
                x.docs = docs
            if title != "":
                x.title = title
            if tv != "":
                x.tv = tvv
            x.save()  # save
            return HttpResponse("uplord successfully")
        except Exception as e:
            print(e)
            return HttpResponse("uplord fail")