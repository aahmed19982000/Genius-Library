from django.shortcuts import render , redirect , get_object_or_404
from django.core.files.storage import FileSystemStorage
from decimal import Decimal
from clients.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


import os
import PyPDF2
import docx
from PIL import Image
from django.core.files.storage import FileSystemStorage


from .forms import UploadForm , OrderChatForm
from .models import Order , OrderChat
from category.models import PaperColor, PaperSize, PaperType , Status
# Create your views here.
#وظيفة تتبع الطلب
def track_order(request):
    order = None
    order_id = request.GET.get('order_id')

    if order_id:
        # إزالة أي رموز غير رقمية مثل #
        order_id_clean = ''.join(filter(str.isdigit, order_id))
        if order_id_clean.isdigit():
            order = Order.objects.filter(id=int(order_id_clean)).first()

    return render(request, 'orders/track_order.html', {'order': order})

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
    client = request.user   # هنا الـ Client اللي عامل تسجيل دخول

    if request.method == 'POST':
        client.full_name = request.POST.get('full_name')
        client.phone = request.POST.get('phone')
        client.address = request.POST.get('address')
        client.notes = request.POST.get('notes')
        client.save()

        request.session['delivery_address'] = client.address
        return redirect('payment_and_confirmation')
    
    return render(request, 'orders/delivery_details.html', {"client": client})

# وظيفة الدفع وتأكيد البيانات
@role_required(allowed_roles=['client'])
def payment_and_confirmation(request):
    # تأكد من أن base_template دايمًا قيمة صحيحة
    base_template = "dashboard_base.html" if getattr(request.user, 'is_staff', False) else "base.html"

    if request.method == 'POST':
        # جلب البيانات من الجلسة مع قيم افتراضية
        file_name = request.session.get('uploaded_file', '')
        paper_type_id = request.session.get('paper_type')
        paper_size_id = request.session.get('paper_size')
        printing_color_id = request.session.get('printing_color')
        printing_sides = request.session.get('printing_sides', '')
        number_of_sheets = int(request.session.get('number_of_sheets', 1))
        quantity = int(request.session.get('quantity', 1))
        notes = request.session.get('notes', '')
        address = request.session.get('delivery_address', '')
        total_cost = request.session.get('total_cost', 0)

        # جلب الكائنات بأمان
        paper_type = PaperType.objects.filter(id=paper_type_id).first() if paper_type_id else None
        paper_size = PaperSize.objects.filter(id=paper_size_id).first() if paper_size_id else None
        printing_color = PaperColor.objects.filter(id=printing_color_id).first() if printing_color_id else None

        # الحالة الافتراضية
        pending_status, _ = Status.objects.get_or_create(status='معلقه')

        # إنشاء الطلب
        order = Order.objects.create(
            client=request.user,
            customer_name=request.user.username,
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
            status=pending_status
        )

        # مسح الجلسة بعد إنشاء الطلب
        request.session.flush()

        return render(request, "orders/order_detail.html", {
            "order": order,
            "base_template": base_template
        })

    # لو GET، عرض البيانات قبل التأكيد
    paper_type_id = request.session.get('paper_type')
    paper_size_id = request.session.get('paper_size')
    printing_color_id = request.session.get('printing_color')

    context = {
        "file_name": request.session.get('uploaded_file', ''),
        "paper_type": PaperType.objects.filter(id=paper_type_id).first().paper_type if paper_type_id else "",
        "paper_size": PaperSize.objects.filter(id=paper_size_id).first().size if paper_size_id else "",
        "printing_color": PaperColor.objects.filter(id=printing_color_id).first().color_paper if printing_color_id else "",
        "printing_sides": request.session.get('printing_sides', ''),
        "number_of_sheets": request.session.get('number_of_sheets', ''),
        "quantity": request.session.get('quantity', ''),
        "address": request.session.get('delivery_address', ''),
        "notes": request.session.get('notes', ''),
        "total_cost": request.session.get('total_cost', 0),
        "base_template": base_template,
    }

    return render(request, "orders/payment_and_confirmation.html", context)


def thank_you(request):
    return render(request, 'orders/thank_you.html')


#وظيفة رسائل الطلبات 
@login_required(login_url="login")
@role_required(allowed_roles=['client', 'admin'])
def orderchat(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # 👈 الشرط: لازم يكون أدمن أو هو صاحب الأوردر
    if not (request.user.is_staff or order.client == request.user):
        return redirect("home")  # أو صفحة "غير مسموح"

    chats = OrderChat.objects.filter(order=order).order_by("created_at")

    # ✅ تعليم الرسائل غير المقروءة كمقروءة
    if request.user.is_staff:
        chats.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    elif order.client == request.user:
        chats.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == "POST":
        form = OrderChatForm(request.POST, request.FILES)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.order = order
            chat.sender = request.user  # سواء كان أدمن أو كلاينت
            chat.save()
            return redirect("orderchat", order_id=order.id)  # عشان مايكرر الإرسال
    else:
        form = OrderChatForm()

    # تحديد القالب الأب
    base_template = "dashboard_base.html" if request.user.is_staff else "base.html"
    
    return render(request, "orders/order_chat.html", {
        "order": order,
        "chats": chats,
        "form": form,
        "base_template": base_template,
    })


# وظيفة عرض كل طلب بشكل منفصل 
@role_required(allowed_roles=['client', 'admin'])
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # لو المستخدم أدمن → يدخل على طول
    if request.user.user_type == 'admin':
        base_template = "dashboard_base.html"
        all_status = Status.objects.all()  # لجلب كل الحالات
    # لو المستخدم عميل → لازم يكون هو صاحب الطلب
    elif request.user.user_type == 'client':
        if order.client != request.user:   # assuming order.client هو FK على Client
            return HttpResponseForbidden("غير مسموح لك برؤية هذا الطلب")
        base_template = "base.html"
        all_status = None  # العملاء لا يمكنهم تعديل الحالة
    else:
        return HttpResponseForbidden("غير مسموح لك برؤية هذا الطلب")

    context = {
        "order": order,
        "base_template": base_template,
        "all_status": all_status,
    }
    return render(request, "orders/order_detail.html", context)


    #وظيفة عرض طلبات العميل المسجل دخول 
@role_required(allowed_roles=['client'])
def client_orders(request):
    orders = Order.objects.filter(client=request.user).order_by("-created_at")
    return render(request, "orders/client_orders.html", {"orders": orders})

    #وظيفة عرض اخر الرسائل الغير مقروءة للادمن
@role_required(allowed_roles=['admin'])
def unread_messages(request):
    unread = OrderChat.objects.filter(is_read=False).exclude(sender=request.user).order_by('-created_at')
    return render(request, 'bakend/unread_messages.html',{"unread": unread})

#وظيفة عرض كل الرسائل للادمن
@role_required(allowed_roles=['admin'])
def message(request):
    unread= OrderChat.objects.order_by('-created_at')
    return render(request, 'bakend/message.html',{"unread": unread})

#وظيفة تعديل حالة الطلب 
@role_required(allowed_roles=['admin'])
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        status_id = request.POST.get('status')
        status_obj = get_object_or_404(Status, id=status_id)  
        order.status = status_obj
        order.save()
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))