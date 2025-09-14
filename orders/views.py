from django.shortcuts import render , redirect
from .forms import UploadForm
# Create your views here.

def track_order(request):
    return render(request, 'orders/track_order.html')

# وظيفة رفع الملفات
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # خزن اسم الملف في الـ session
            request.session['uploaded_file_name'] = form.cleaned_data['file'].name
            
            # بعد رفع الملف بنروح لاختيار الورق
            return redirect('choose_paper')
        else:
            # لو الفورم فيه أخطاء، نرجع لنفس صفحة الرفع مع عرض الأخطاء
            return render(request, 'orders/upload.html', {'form': form})
    else:
        # أول مرة يفتح الصفحة (GET)
        form = UploadForm()
    
    # اعرض صفحة الرفع
    return render(request, 'orders/upload.html', {'form': form})


# وظيفة اختيار نوع الورق
def choose_paper(request):
    upload_file = request.session.get('uploaded_file_name')
    
    if request.method == 'POST':
        # هنا ممكن تخزن نوع الورق المختار في الـ session
        request.session['type_papers'] = request.POST.get('type_papers')
        return redirect('delivery_details')
    
    return render(request, 'orders/choose_paper.html', {
        "upload_file": upload_file
    })


# وظيفة تفاصيل الشحن
def delivery_details(request):
    if request.method == 'POST':
        # هنا هتخزن بيانات الشحن في الـ session أو DB
        request.session['delivery_address'] = request.POST.get('address')
        return redirect('payment_and_confirmation')
    
    return render(request, 'orders/delivery_details.html')


# وظيفة الدفع وتأكيد البيانات
def payment_and_confirmation(request):
    return render(request, 'orders/payment_and_confirmation.html')
