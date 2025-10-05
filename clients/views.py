from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login

#  انشاء حساب على الموقع

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'clients/success.html')
    else:
        form = CustomUserCreationForm()

    return render(request, 'clients/register.html', {"form": form})





def login_view(request):
    next_url = request.GET.get("next")  # بنجيب الصفحة اللي المستخدم حاول يدخل عليها

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # تسجيل الدخول

            # ✅ لو فيه صفحة مطلوب يرجع لها
            if next_url:
                return redirect(next_url)

            # ✅ لو مفيش، وجهه حسب نوع الحساب
            if user.user_type == 'admin':
                return redirect("dashboard")
            else:  # client
                return redirect("my_orders")

        else:
            # لو فيه خطأ → رجّع الرسالة مع next
            return render(request, "clients/login.html", {
                "error": "❌ اسم المستخدم أو كلمة المرور غلط",
                "username": username,
                "next": next_url,
            })

    return render(request, "clients/login.html", {"next": next_url})



def no_permission(request):
    return render(request, 'no_permission.html')