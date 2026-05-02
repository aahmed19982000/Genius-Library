from rest_framework import serializers
from django.contrib.auth import get_user_model

# استيراد الموديل المستخدم حالياً (Client)
User = get_user_model()

# محاولة استيراد Notification من ملف الموديلات الرئيسي في تطبيق clients
try:
    from clients.models import Notification
except ImportError:
    Notification = None

# 1. سيرايليز الخاص بالمستخدم (متوافق مع موديل Client الجديد)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'address', 
            'user_type'
        ]
        read_only_fields = ['id']

# 2. سيرايليز تسجيل مستخدم جديد
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'confirm', 
            'first_name', 'last_name', 'phone_number', 
            'address', 'user_type'
        ]

    def validate(self, data):
        if data['password'] != data['confirm']:
            raise serializers.ValidationError({"password": "كلمات المرور غير متطابقة."})
        return data

    def create(self, validated_data):
        # حذف confirm قبل الحفظ
        validated_data.pop('confirm')
        
        # إنشاء المستخدم باستخدام create_user لضمان تشفير كلمة المرور
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', ''),
            user_type=validated_data.get('user_type', 'client')
        )
        return user

# 3. سيرايليز الخاص بالإشعارات
if Notification:
    class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Notification
            fields = ['id', 'user', 'message', 'is_read', 'created_at']
            read_only_fields = ['id', 'created_at']
else:
    # كلاس احتياطي في حال عدم وجود موديل Notification لمنع انهيار الـ Views
    class NotificationSerializer(serializers.Serializer):
        message = serializers.CharField()