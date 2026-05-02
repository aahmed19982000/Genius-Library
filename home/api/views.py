from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model

# استيراد الموديلات
User = get_user_model()

# سنحاول استيراد Notification، إذا لم تكن موجودة لن يتعطل الملف بالكامل
try:
    from ..models import Notification
except ImportError:
    Notification = None

from .serializers import UserSerializer, RegisterSerializer, NotificationSerializer

# 1. تسجيل الدخول والحصول على Token
class APILoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                'user': UserSerializer(user).data,
                'user_type': user.user_type  # تم التعديل من role لـ user_type
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'بيانات الدخول غير صحيحة'}, status=status.HTTP_401_UNAUTHORIZED)

# 2. إنشاء مستخدم جديد (للأدمن فقط)
class APISignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def create(self, request, *args, **kwargs):
        # تم التعديل ليتوافق مع choices: 'admin'
        if request.user.user_type != 'admin':
            return Response({'error': 'ليس لديك صلاحية أدمن لإنشاء مستخدم'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

# 3. عرض قائمة العملاء وحذفهم
class APIEmployeeListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class APIEmployeeDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        if request.user.user_type != 'admin':
            return Response({'error': 'ليس لديك صلاحية للحذف'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

# 4. التعامل مع الإشعارات (تعمل فقط إذا وجد الموديل)
class APINotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if Notification:
            return Notification.objects.filter(user=self.request.user)
        return []

class APINotificationActionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, action):
        if not Notification:
            return Response({'error': 'موديل الإشعارات غير مفعل'}, status=status.HTTP_404_NOT_FOUND)
            
        try:
            notification = Notification.objects.get(id=pk, user=request.user)
            if action == 'mark-read':
                notification.is_read = True
                notification.save()
                return Response({'status': 'notification marked as read'})
            elif action == 'delete':
                notification.delete()
                return Response({'status': 'notification deleted'})
            return Response({'error': 'invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        except Notification.DoesNotExist:
            return Response({'error': 'not found'}, status=status.HTTP_404_NOT_FOUND)