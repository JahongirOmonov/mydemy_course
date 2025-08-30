from django.shortcuts import render
from .models import Order
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER

class OrderApiViews(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            context = {
                'data':serializer.data,
                'message':'All orders taken successfully'
            }
            return Response(context, status=status.HTTP_200_OK)
        except:
            context = {
                'data':{},
                'message':'Something went wrong!'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    # def post(self, request):
    #     try:
    #         data = request.data
    #         serializer = OrderSerializer(data=data)
    #         if serializer.is_valid():

    #             subject = 'New order is placed'
    #             message = 'Dear customer '+data['customer_name'] + ' your order is placed now, thanks for your order'
    #             recipient_list = [data['customer_email']]
    #             send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)

    #             serializer.save()
    #             context = {
    #             'data':serializer.data,
    #             'message':'Order created successfully'
    #         }
    #         return Response(context, status=status.HTTP_201_CREATED)
    #     except:
    #         context = {
    #             'data':serializer.errors,
    #             'message':'something went wrong'
    #         }
    #         return Response(context, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        # 1) Avval VALIDATSIA — xato bo'lsa xatolarni ko'rsatib qaytamiz
        if not serializer.is_valid():
            return Response(
                {"data": serializer.errors, "message": "validation error"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Ma'lumotni saqlaymiz
        order = serializer.save()

        # 3) Email jo'natish (ixtiyoriy). Xato bo'lsa API yiqilmasin.
        try:
            subject = "New order is placed"
            message = f"Dear customer {order.customer_name}, your order is placed now, thanks for your order"
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or getattr(settings, "EMAIL_HOST_USER", None)
            if from_email:
                send_mail(subject, message, from_email, [order.customer_email], fail_silently=True)
        except Exception as e:
            # Bu yerda log yozib qo'ying, lekin javobni buzmaymiz
            print("Send mail error:", e)

        return Response(
            {"data": OrderSerializer(order).data, "message": "Order created successfully"},
            status=status.HTTP_201_CREATED
        )
        
    def patch(self, request):
        try:
            data= request.data
            order = Order.objects.filter(id=data.get('id'))
            if not order.exists():
                context = {
                'data':{},
                'message':'wrong ID'
            }
                return Response(context, status=status.HTTP_404_NOT_FOUND)
            serializer = OrderSerializer(order[0], data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {
                'data':serializer.data,
                'message':'all okay'
            }
                return Response(context, status=status.HTTP_206_PARTIAL_CONTENT)
            else:
                context = {
                'data':serializer.errors,
                'message':'all not okay'
            }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except:
            context = {
                'data':serializer.errors,
                'message':'all not okay'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        data = request.data
        order_id = data.get('id')
        if not order_id:
            return Response({'message':'Qandaydir son kirit ID uchun'})
        try:

            order = Order.objects.get(id=order_id)
            order.delete()
            return Response({"message":"Successfully deleted!"})
        except:
            context = {'message':'There is no order with this ID'}
            return Response(context)
       





