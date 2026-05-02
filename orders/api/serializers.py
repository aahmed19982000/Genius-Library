from rest_framework import serializers
from orders.models import Order, OrderChat
from category.models import PaperType, PaperSize, PaperColor, Status

class PaperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperType
        fields = ['id', 'paper_type', 'price']

class PaperSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperSize
        fields = ['id', 'size', 'price']

class PaperColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperColor
        fields = ['id', 'color_paper', 'price']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'status']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'file_name', 'paper_type',
            'paper_size', 'printing_color', 'printing_sides',
            'number_of_sheets', 'quantity', 'address', 'notes',
            'total_cost', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'total_cost', 'status', 'created_at', 'customer_name']

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'file_name', 'paper_type', 'paper_size', 'printing_color',
            'printing_sides', 'number_of_sheets', 'quantity', 'address', 'notes'
        ]

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        paper_type = validated_data.get('paper_type')
        paper_size = validated_data.get('paper_size')
        printing_color = validated_data.get('printing_color')
        printing_sides = validated_data.get('printing_sides', 'one side')
        number_of_sheets = validated_data.get('number_of_sheets', 1)
        quantity = validated_data.get('quantity', 1)

        from decimal import Decimal
        price = Decimal('0.00')
        if paper_type:
            price += Decimal(str(paper_type.price))
        if paper_size:
            price += Decimal(str(paper_size.price))
        if printing_color:
            price += Decimal(str(printing_color.price))
        if printing_sides == 'tow side':
            price *= Decimal('1.5')

        total_cost = price * number_of_sheets * quantity

        pending_status, _ = Status.objects.get_or_create(status='معلقه')

        order = Order.objects.create(
            client=user,
            customer_name=user.username,
            total_cost=total_cost,
            status=pending_status,
            **validated_data
        )
        return order