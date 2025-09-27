from django.shortcuts import render ,redirect , get_object_or_404
from .models import PaperColor , PaperType , PaperSize
from .forms import PaperColorForm , PaperTypeForm ,PaperSizeForm

#وظيفة عرض كل الالوان 
def paper_colors(request):
    colors = PaperColor.objects.all()
    color_id = request.GET.get('edit')
    delete_id = request.GET.get('delete')
    form = None
    edit_color_obj = None

    # حذف اللون
    if delete_id:
        color = get_object_or_404(PaperColor, id=delete_id)
        color.delete()
        return redirect('paper_colors')

    # تعديل اللون
    if color_id:
        edit_color_obj = get_object_or_404(PaperColor, id=color_id)
        if request.method == 'POST':
            form = PaperColorForm(request.POST, instance=edit_color_obj)
            if form.is_valid():
                form.save()
                return redirect('paper_colors')
        else:
            form = PaperColorForm(instance=edit_color_obj)
    # إضافة لون جديد
    else:
        if request.method == 'POST':
            form = PaperColorForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('paper_colors')
        else:
            form = PaperColorForm()

    return render(request, 'bakend/paper_colors.html', {
        'colors': colors,
        'form': form,
        'edit_color_obj': edit_color_obj,
    })

#عروض كل الورق والتعديل عليه
def paper_types(request):
    types = PaperType.objects.all()
    type_id = request.GET.get('edit')
    delete_id = request.GET.get('delete')
    form = None
    edit_type_obj = None

   #حذف النوع 
    if delete_id:
     type = get_object_or_404(PaperType, id=delete_id)
     type.delete()
     return redirect('paper_types')

     #تعديل النوع
    if type_id:
     edit_type_obj = get_object_or_404(PaperType, id=type_id)
     if request.method == 'POST':
         form =PaperTypeForm(request.POST, instance=edit_type_obj)
         if form.is_valid():
             form.save()
             return redirect('paper_types')
         else:
             form = PaperTypeForm(instance=edit_type_obj)
        
    #اضافة نوع جديد
    else:
        if request.method == 'POST':
            form = PaperTypeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('paper_types')
        else:
            form = PaperTypeForm()


    return render (request, 'bakend/paper_types.html',{
        'types' : types,
        'form' : form,
        'edit_type_obj': edit_type_obj
    })

#عرض كل المقسات والتعديل عليها 

def papersize(request):
    sizes = PaperSize.objects.all()  # كل المقاسات
    size_id = request.GET.get('edit')
    delete_id = request.GET.get('delete')

    form = None
    edit_size_obj = None

    # حذف المقاس
    if delete_id:
        obj = get_object_or_404(PaperSize, id=delete_id)
        obj.delete()
        return redirect('papersize')

    # تعديل المقاس
    if size_id:
        edit_size_obj = get_object_or_404(PaperSize, id=size_id)
        if request.method == 'POST':
            form = PaperSizeForm(request.POST, instance=edit_size_obj)
            if form.is_valid():
                form.save()
                return redirect('papersize')
        else:
            form = PaperSizeForm(instance=edit_size_obj)

    # إضافة مقاس جديد
    else:
        if request.method == 'POST':
            form = PaperSizeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('papersize')
        else:
            form = PaperSizeForm()

    context = {
        'sized': sizes,
        'form': form,
        'edit_size_obj': edit_size_obj,
    }
    return render(request, 'bakend/papersize.html', context)
