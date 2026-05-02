from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import Order
from category.models import PaperType, PaperSize, PaperColor
from .serializers import (
    OrderSerializer, OrderCreateSerializer,
    PaperTypeSerializer, PaperSizeSerializer, PaperColorSerializer
)
import PyPDF2  # ✅ أضف الاستيراد


class PaperOptionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'paper_types': PaperTypeSerializer(PaperType.objects.all(), many=True).data,
            'paper_sizes': PaperSizeSerializer(PaperSize.objects.all(), many=True).data,
            'paper_colors': PaperColorSerializer(PaperColor.objects.all(), many=True).data,
            'printing_sides': [
                {'value': 'one side', 'label': 'وجه واحد'},
                {'value': 'tow side', 'label': 'وجهين'},
            ]
        })


class CountPagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "لم يتم إرسال ملف"}, status=400)

        try:
            ext = file.name.lower().split(".")[-1]

            if ext == "pdf":
                reader = PyPDF2.PdfReader(file)
                pages = len(reader.pages)

            elif ext in ("jpg", "jpeg", "png"):
                pages = 1

            elif ext == "docx":
                from docx import Document
                doc = Document(file)
                words = sum(len(p.text.split()) for p in doc.paragraphs)
                pages = max(1, words // 250)

            else:
                pages = 1

            return Response({"pages": pages})

        except Exception as e:
            return Response({"pages": 1, "error": str(e)}, status=200)


class OrderCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ClientOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).order_by('-created_at')