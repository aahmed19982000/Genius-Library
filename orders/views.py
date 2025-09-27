from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage

from .forms import UploadForm
from .models import Order
from category.models import PaperColor, PaperSize, PaperType
# Create your views here.

def track_order(request):
    return render(request, 'orders/track_order.html')

# وظيفة رفع الملفات
def upload_file(request):
      if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            
            # خزّن الملف فعليًا في MEDIA_ROOT
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)

            # خزّن اسم الملف و الرابط في session
            request.session['uploaded_file'] = filename
            request.session['uploaded_file_url'] = file_url

            return redirect('choose_paper')
        else:
            return render(request, 'orders/upload.html', {'form': form})
      else:
        form = UploadForm()
      return render(request, 'orders/upload.html', {'form': form})

# وظيفة اختيار نوع الورق
def choose_paper(request):
    upload_file = request.session.get('uploaded_file')

    # تمرير القوائم الديناميكية من الموديل
    paper_type_choices = PaperType.objects.all()
    paper_size_choices =PaperSize.objects.all()
    printing_color_choices = PaperColor.objects.all()
    printing_sides_choices = Order.PAPER_SIDES

    # تحويل القيم إلى نص عربي
    paper_type_dict = {pt.id: pt.paper_type for pt in PaperType.objects.all()}
    paper_size_dict = {ps.id: ps.size for ps in PaperSize.objects.all()}
    printing_color_dict = {pc.id: pc.color_paper for pc in PaperColor.objects.all()}
    printing_sides_dict = dict(Order.PAPER_SIDES)

    if request.method == 'POST':
        request.session['paper_type'] = paper_type_dict.get(request.POST.get('paper_type'), request.POST.get('paper_type'))
        request.session['paper_size'] = paper_size_dict.get(request.POST.get('paper_size'), request.POST.get('paper_size'))
        request.session['printing_color'] = printing_color_dict.get(request.POST.get('printing_color'), request.POST.get('printing_color'))
        request.session['printing_sides'] = printing_sides_dict.get(request.POST.get('printing_sides'), request.POST.get('printing_sides'))
        request.session['number_of_sheets'] = request.POST.get('number_of_sheets')
        request.session['quantity'] = request.POST.get('quantity')
        request.session['notes'] = request.POST.get('notes')
        return redirect('delivery_details')

    return render(request, 'orders/choose_paper.html', {
        "upload_file": upload_file,
        "paper_type_choices": paper_type_choices,
        "paper_size_choices": paper_size_choices,
        "printing_color_choices": printing_color_choices,
        "printing_sides_choices": printing_sides_choices,
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
    if request.method == 'POST':
        # اجمع البيانات من الـ session
        file_name = request.session.get('uploaded_file')
        paper_type_id = request.session.get('paper_type')
        paper_size_id = request.session.get('paper_size')
        printing_color_id = request.session.get('printing_color')
        printing_sides = request.session.get('printing_sides')
        number_of_sheets = request.session.get('number_of_sheets')
        quantity = request.session.get('quantity')
        notes = request.session.get('notes')
        address = request.session.get('delivery_address')

        # أنشئ الطلب في DB باستخدام IDs
        order = Order.objects.create(
            customer_name="زائر الموقع",
            file_name=file_name,
            paper_type=PaperType.objects.get(id=paper_type_id) if paper_type_id else None,
            paper_size=PaperSize.objects.get(id=paper_size_id) if paper_size_id else None,
            printing_color=PaperColor.objects.get(id=printing_color_id) if printing_color_id else None,
            printing_sides=printing_sides,
            number_of_sheets=number_of_sheets,
            quantity=quantity,
            address=address,
            notes=notes,
            status="pending"
        )

        # امسح الـ session
        request.session.flush()

        return render(request, "orders/thank_you.html", {"order": order})

    # لو الطلب GET (عرض ملخص الطلب قبل الدفع)
    paper_type_id = request.session.get('paper_type')
    paper_size_id = request.session.get('paper_size')
    printing_color_id = request.session.get('printing_color')

    context = {
        "file_name": request.session.get('uploaded_file'),
        "paper_type": PaperType.objects.get(id=paper_type_id).paper_type if paper_type_id else "",
        "paper_size": PaperSize.objects.get(id=paper_size_id).size if paper_size_id else "",
        "printing_color": PaperColor.objects.get(id=printing_color_id).color_paper if printing_color_id else "",
        "printing_sides": request.session.get('printing_sides'),
        "number_of_sheets": request.session.get('number_of_sheets'),
        "quantity": request.session.get('quantity'),
        "address": request.session.get('delivery_address'),
        "notes": request.session.get('notes'),
    }

    return render(request, "orders/payment_and_confirmation.html", context)


def thank_you(request):
    return render(request, 'orders/thank_you.html')
