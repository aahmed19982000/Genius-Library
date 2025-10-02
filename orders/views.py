from django.shortcuts import render , redirect , get_object_or_404
from django.core.files.storage import FileSystemStorage
from decimal import Decimal
from clients.decorators import role_required
from django.http import HttpResponseForbidden


import os
import PyPDF2
import docx
from PIL import Image
from django.core.files.storage import FileSystemStorage


from .forms import UploadForm , OrderChatForm
from .models import Order , OrderChat
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

            # --- تحديد عدد الصفحات ---
            num_pages = 1  # القيمة الافتراضية
            ext = os.path.splitext(uploaded_file.name)[1].lower()  # الامتداد

            if ext == ".pdf":
                pdf_path = fs.path(filename)
                with open(pdf_path, 'rb') as pdf_file:
                    reader = PyPDF2.PdfReader(pdf_file)
                    num_pages = len(reader.pages)

            elif ext == ".docx":
                doc_path = fs.path(filename)
                doc = docx.Document(doc_path)
                # هنا ممكن تعتبر كل 500 كلمة = صفحة تقريبية
                word_count = sum(len(p.text.split()) for p in doc.paragraphs)
                num_pages = max(1, word_count // 500)

            elif ext in [".jpg", ".jpeg", ".png", ".tiff"]:
                # كل صورة = صفحة واحدة
                num_pages = 1

            # لو عايز تضيف txt
            elif ext == ".txt":
                txt_path = fs.path(filename)
                with open(txt_path, 'r', encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                # كل 40 سطر = صفحة تقريبية
                num_pages = max(1, len(lines) // 40)

            # خزّن البيانات في session
            request.session['uploaded_file'] = filename
            request.session['uploaded_file_url'] = file_url
            request.session['number_of_sheets'] = num_pages

            return redirect('choose_paper')
        else:
            return render(request, 'orders/upload.html', {'form': form})
    else:
        form = UploadForm()
    return render(request, 'orders/upload.html', {'form': form})

# وظيفة اختيار نوع الورق
@role_required(allowed_roles=['client'])
def choose_paper(request):
    upload_file = request.session.get('uploaded_file')

    # القيمة الافتراضية لعدد الصفحات (من الرفع)
    default_sheets = request.session.get('number_of_sheets', 1)

    # تمرير القوائم الديناميكية من الموديل
    paper_type_choices = PaperType.objects.all()
    paper_size_choices = PaperSize.objects.all()
    printing_color_choices = PaperColor.objects.all()
    printing_sides_choices = Order.PAPER_SIDES

    if request.method == 'POST':
        paper_type_id = request.POST.get('paper_type')
        paper_size_id = request.POST.get('paper_size')
        printing_color_id = request.POST.get('printing_color')
        printing_sides = request.POST.get('printing_sides')
        number_of_sheets = int(request.POST.get('number_of_sheets', default_sheets))
        quantity = int(request.POST.get('quantity', 1))
        notes = request.POST.get('notes')

        # هات الكائنات من الـ DB
        paper_type = PaperType.objects.get(id=paper_type_id) if paper_type_id else None
        paper_size = PaperSize.objects.get(id=paper_size_id) if paper_size_id else None
        printing_color = PaperColor.objects.get(id=printing_color_id) if printing_color_id else None

        # حساب السعر
        price_per_sheet = Decimal('0.00')
        if paper_type:
            price_per_sheet += Decimal(paper_type.price)
        if paper_size:
            price_per_sheet += Decimal(paper_size.price)
        if printing_color:
            price_per_sheet += Decimal(printing_color.price)

        if printing_sides == 'وجهين':
            price_per_sheet *= Decimal('1.5')

        total_cost = price_per_sheet * number_of_sheets * quantity

        # خزّن كل القيم في الـ session
        request.session['paper_type'] = paper_type_id
        request.session['paper_size'] = paper_size_id
        request.session['printing_color'] = printing_color_id
        request.session['printing_sides'] = printing_sides
        request.session['number_of_sheets'] = number_of_sheets
        request.session['quantity'] = quantity
        request.session['notes'] = notes
        request.session['total_cost'] = float(total_cost)

        # DEBUG
        print("PaperType price:", paper_type.price if paper_type else 0)
        print("PaperSize price:", paper_size.price if paper_size else 0)
        print("PrintingColor price:", printing_color.price if printing_color else 0)
        print("Price per sheet:", price_per_sheet)
        print("Sheets:", number_of_sheets, "Quantity:", quantity)
        print("Total:", total_cost)

        return redirect('delivery_details')

    return render(request, 'orders/choose_paper.html', {
        "upload_file": upload_file,
        "paper_type_choices": paper_type_choices,
        "paper_size_choices": paper_size_choices,
        "printing_color_choices": printing_color_choices,
        "printing_sides_choices": printing_sides_choices,
        'default_sheets': default_sheets,  
    })
# وظيفة تفاصيل الشحن
@role_required(allowed_roles=['client'])
def delivery_details(request):
    if request.method == 'POST':
        # هنا هتخزن بيانات الشحن في الـ session أو DB
        request.session['delivery_address'] = request.POST.get('address')
        return redirect('payment_and_confirmation')
    
    return render(request, 'orders/delivery_details.html')



# وظيفة الدفع وتأكيد البيانات
@role_required(allowed_roles=['client'])
def payment_and_confirmation(request):
    if request.method == 'POST':
        file_name = request.session.get('uploaded_file')
        paper_type_id = request.session.get('paper_type')
        paper_size_id = request.session.get('paper_size')
        printing_color_id = request.session.get('printing_color')
        printing_sides = request.session.get('printing_sides')
        number_of_sheets = int(request.session.get('number_of_sheets', 1))
        quantity = int(request.session.get('quantity', 1))
        notes = request.session.get('notes')
        address = request.session.get('delivery_address')
        total_cost = request.session.get('total_cost', 0)

        # هات الكائنات
        paper_type = PaperType.objects.get(id=paper_type_id) if paper_type_id else None
        paper_size = PaperSize.objects.get(id=paper_size_id) if paper_size_id else None
        printing_color = PaperColor.objects.get(id=printing_color_id) if printing_color_id else None

        # أنشئ الطلب
        order = Order.objects.create(
            client=request.user,
            file_name=file_name,
            paper_type=paper_type,
            paper_size=paper_size,
            printing_color=printing_color,
            printing_sides=printing_sides,
            number_of_sheets=number_of_sheets,
            quantity=quantity,
            address=address,
            notes=notes,
            total_cost=total_cost,
            status="pending"
        )

        request.session.flush()
        return render(request, "orders/order_detail.html", {"order": order})

    # لو GET
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
        "total_cost": request.session.get('total_cost'),
    }

    return render(request, "orders/payment_and_confirmation.html", context)


def thank_you(request):
    return render(request, 'orders/thank_you.html')


#وظيفة رسائل الطلبات 
@role_required(allowed_roles=['client', 'admin'])
def orderchat(request, order_id):
    order = Order.objects.get(id=order_id)
    chats = OrderChat.objects.filter(order= order).order_by("created_at")

    if request.method == "POST":
        form = OrderChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.order = order
            chat.sender = request.user  or  client.role =='admin'
            chat.save()
            return redirect("orderchat", order_id=order.id)  # عشان مايكرر الإرسال
    else:
        form = OrderChatForm()
    
    return render(request, "orders/order_chat.html", {
        "order": order,
        "chats": chats,
        "form": form
    })

# وظيفة عرض كل طلب بشكل منفصل 
@role_required(allowed_roles=['client', 'admin'])
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # لو المستخدم أدمن → يدخل على طول
    if request.user.user_type == 'admin':
        pass

    # لو المستخدم عميل → لازم يكون هو صاحب الطلب
    elif request.user.user_type == 'client':
        if order.client != request.user:   # assuming order.client هو FK على Client
            return HttpResponseForbidden("غير مسموح لك برؤية هذا الطلب")

    else:
        return HttpResponseForbidden("غير مسموح لك برؤية هذا الطلب")

    context = {"order": order}
    return render(request, "orders/order_detail.html", context)


    #وظيفة عرض طلبات العميل المسجل دخول 
@role_required(allowed_roles=['client'])
def client_orders(request):
    orders = Order.objects.filter(client=request.user).order_by("-created_at")
    return render(request, "orders/client_orders.html", {"orders": orders})