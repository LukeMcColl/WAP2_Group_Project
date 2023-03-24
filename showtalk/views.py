from django.shortcuts import render, redirect
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotAllowed,
    HttpResponsePermanentRedirect,
)
from django.urls import reverse
from typing import Optional

from showtalk.forms import UserForm
from showtalk.models import user, tv, pl


def reverse_redirect(route_name: str, *args, **kwargs) -> HttpResponsePermanentRedirect:
    return redirect(reverse(route_name, *args, **kwargs))


def homepage(request, page_id: int = None):
    if request.method == "GET":
        single_show = bool(page_id)
        print(page_id)
        context = {
            "single_show": single_show,
            "shows": [tv.objects.get(id=page_id)] if single_show else tv.objects.all,
            # Translation note: "pinglun" is Chinese for "comment"
            "comments": pl.objects.filter(tv_id=page_id) if single_show else [],
        }
        return render(request, "showtalk/homepage.html", context=context)


def register(request):
    if request.method == "GET":
        return render(request, "login/register.html")

    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        password = request.POST.get("password")

        up_sql = user.objects.create(username=username, name=name, password=password)
        up_tv = tv.objects.create(
            user_id=up_sql.id, title="default video", docs="default info"
        )
        return render(
            request,
            "feedback.html",
            context={"success": True, "action_name": "Registration"},
        )


def logout(request):
    if "username" in request.session:
        del request.session["username"]
    if "uid" in request.session:
        del request.session["uid"]
    if "name" in request.session:
        del request.session["name"]
    resp = reverse_redirect("showtalk:homepage")
    return resp


def login(request):
    if request.method == "GET":
        if request.session.get("username"):
            return render(
                request,
                "feedback.html",
                context={
                    "success": False,
                    "action_name": "Login",
                    "extra_message": "You are already logged in.",
                },
            )

        else:
            return render(request, "login/login.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            test = user.objects.get(username=username, password=password)
            request.session["username"] = test.username
            request.session["uid"] = test.id

            request.session["name"] = test.name
        except:
            return render(
                request,
                "feedback.html",
                context={"success": False, "action_name": "Login"},
            )

        return reverse_redirect("showtalk:homepage")


def get_session_uid(request: HttpRequest) -> Optional[int]:
    return request.session.get("uid")


def profile(request: HttpRequest) -> HttpResponse:
    ALLOWED_METHODS = ["GET", "POST"]
    if request.method not in ALLOWED_METHODS:
        return HttpResponseNotAllowed(ALLOWED_METHODS)

    uid = get_session_uid(request)
    if not uid:
        return reverse_redirect("showtalk:login")
    current_user = user.objects.get(id=uid)

    if request.method == "POST":
        form = UserForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            return render(
                request,
                "feedback.html",
                context={"success": True, "action_name": "Profile update"},
            )
    else:  # GET
        form = UserForm(instance=current_user)

    return render(
        request, "showtalk/profile.html", context={"form": form, "user": current_user}
    )


def pinglun(request):
    if request.method == "POST":
        pinglun = request.POST.get("pinglun")
        uid = request.session.get("uid")
        tvid = request.POST.get("id")
        try:
            pl.objects.create(doc=pinglun, user_id=uid, tv_id=tvid)
            return render(
                request,
                "feedback.html",
                context={"success": True, "action_name": "Post"},
            )

        except:
            return render(
                request,
                "feedback.html",
                context={"success": False, "action_name": "Post"},
            )


def tvv(request):
    if request.method == "GET":
        try:
            uid = request.session.get("uid")
            tvall = tv.objects.filter(user_id=uid)
        except:
            return reverse_redirect("showtalk:login")

        return render(request, "showtalk/tv.html", locals())

    if request.method == "POST":
        uid = request.session.get("uid")

        title = request.POST.get("title")
        docs = request.POST.get("docs")
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
            return render(
                request,
                "feedback.html",
                context={"success": True, "action_name": "Upload"},
            )
        except Exception as e:
            print(e)
            return render(
                request,
                "feedback.html",
                context={"success": False, "action_name": "Upload"},
            )


def find_show(request: HttpRequest) -> HttpResponse:
    go_home = reverse_redirect("showtalk:homepage")
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    query = request.POST.get("query")
    if not query:
        return go_home

    matches = tv.objects.filter(title__contains=query)
    return (
        reverse_redirect("showtalk:homepage", kwargs={"page_id": matches[0].id})
        if matches
        else go_home
    )
