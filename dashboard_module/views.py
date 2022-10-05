import json
from decimal import Decimal
import time
import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, DetailView

from dashboard_module.forms import UserInfoForm, Checkoutins, CheckoutForm, ImageForm
from polls.templatetags.poll_extras import Price_Format
# Create your views here.
from django.template.loader import render_to_string

from dashboard_module.models import Cart, Item, Discountcodes, UserInfo, UserDiscountCode
from store_module.models import Product



def cart(request):
    cart , created = Cart.objects.prefetch_related("item_set").get_or_create(user_id=request.user.id , status=True)
    items = cart.item_set.filter(product__status = True)
    items_false = cart.item_set.filter(product__status = False)
    items_false.delete()
    context = {
        'items':items,
        'cart':cart

    }
    return render(request , 'dashboard_module/cart.html' , context)



def AddtoCart(request):
    data = request.POST
    quantity = data.get('quantity')
    product_id = data.get("product_id")
    user_id = request.user.id
    if not request.user.is_authenticated:
        return JsonResponse({'status':'userid not found'})

    product = Product.objects.filter(id=product_id, status=True).exists()
    if product:
        if Product.objects.filter(id=product_id, status=True , quantity__gte=quantity).exists():

            cart, created = Cart.objects.get_or_create(status=True, user_id=user_id)
            item = Item.objects.filter(cart_id=cart.id, product_id=product_id).first()

            if item is not None:
                item.quantity += int(quantity)
                item.save()
            else:
                Item.objects.create(cart_id=cart.id, product_id=product_id, quantity=quantity)
            count = Cart.objects.filter(status=True, user_id=user_id).first().item_set.count()

            return JsonResponse({'status': 'successful', 'count_p': count})
        else:
            return JsonResponse({'status': 'There is not enough stock'})
    else:
        return JsonResponse({'status': 'product not found'})


# def Checkout(request):
#
#
#     cart, created = Cart.objects.prefetch_related("item_set").get_or_create(user_id=request.user.id, status=True)
#     items = cart.item_set.filter(product__status=True)
#     items_false = cart.item_set.filter(product__status=False)
#     items_false.delete()
#     user = User.objects.get(id=request.user.id)
#     form_checkout = UserInfoForm(instance=user)
#     context = {
#         'items':items,
#         'cart':cart,
#         'form':form_checkout
#     }
#     return render(request, 'dashboard_module/checkout.html', context)







# class Checkout(View):
#
#     def get(self, request):
#
#         cart, created = Cart.objects.prefetch_related("item_set").get_or_create(user_id=request.user.id, status=True)
#         items = cart.item_set.filter(product__status=True)
#         items_false = cart.item_set.filter(product__status=False)
#         items_false.delete()
#         userinfo = UserInfo.objects.get(user_id=request.user.id)
#         form_checkout = CheckoutForm(instance=userinfo)
#         user = User.objects.get(id=request.user.id)
#         form_extra = Checkoutins(instance=user)
#
#         discount_code = UserDiscountCode.objects.filter(cart_id=cart.id)
#         if discount_code.first() is not None:
#             persent = discount_code.first().code.discount
#             total_price = cart.total
#             final_price = total_price - (total_price * (persent / Decimal('100')))
#             final_price = format(final_price, '.2f')
#         else:
#             final_price = None
#             persent = None
#
#         context = {
#             'items':items,
#             'cart':cart,
#             'form':form_checkout,
#             'form2':form_extra,
#             'discount_code':discount_code.exists(),
#             'persent':persent,
#             'final_price':final_price
#         }
#         return render(request, 'dashboard_module/checkout.html', context)
#
#
#
#     def post(self , request):
#
#         cart, created = Cart.objects.prefetch_related("item_set").get_or_create(user_id=request.user.id, status=True)
#         checkoutform = CheckoutForm(request.POST)
#         items = cart.item_set.filter(product__status=True)
#         items_false = cart.item_set.filter(product__status=False)
#         items_false.delete()
#         userinfo = UserInfo.objects.get(user_id=request.user.id)
#         form_checkout = CheckoutForm(instance=userinfo)
#         user = User.objects.get(id=request.user.id)
#         form_extra = Checkoutins(instance=user)
#         if checkoutform.is_valid():
#
#             cart.address = checkoutform.cleaned_data.get('address')
#             cart.Country = checkoutform.cleaned_data.get('Country')
#             cart.firstname = checkoutform.cleaned_data.get('firstname')
#             cart.lastname = checkoutform.cleaned_data.get('lastname')
#             cart.State = checkoutform.cleaned_data.get('State')
#             cart.zip = checkoutform.cleaned_data.get('zip')
#             cart.save()
#             dicount = UserDiscountCode.objects.filter(cart_id=cart.id).first()
#             if dicount is not None:
#                 discount_code = True
#                 persent = dicount.code.discount
#                 total_price = cart.total
#                 final_price = total_price - (total_price * (persent / Decimal('100')))
#             else:
#                 discount_code = False
#                 final_price = None
#                 persent = None
#
#
#
#
#             context = {
#                 'items': items,
#                 'cart': cart,
#                 'form': form_checkout,
#                 'form2': form_extra,
#                 'discount_code': discount_code,
#                 'persent': persent,
#                 'final_price': final_price
#             }
#             return render(request, 'dashboard_module/checkout.html', context)
#
#
#
#         context = {
#             'items': items,
#             'cart': cart,
#             'form': form_checkout,
#             'form2': form_extra,
#
#         }
#
#         return render(request , 'dashboard_module/checkout.html' , context)



# class Checkout(CreateView):
#     template_name = 'dashboard_module/checkout.html'
#     form_class = CheckoutForm
#
#     def get_context_data(self, **kwargs):
#         context = super(Checkout, self).get_context_data(**kwargs)
#         cart, created = Cart.objects.prefetch_related("item_set").get_or_create(user_id=self.request.user.id, status=True)
#         items = cart.item_set.filter(product__status=True)
#         items_false = cart.item_set.filter(product__status=False)
#         items_false.delete()
#         context['cart'] = cart
#         context['items'] = items
#         dicount = UserDiscountCode.objects.filter(cart_id=cart.id).first()
#         if dicount is not None:
#             discount_code = True
#             persent = dicount.code.discount
#             total_price = cart.total
#             final_price = total_price - (total_price * (persent / Decimal('100')))
#             context['discount_code'] = discount_code
#             context['final_price'] = final_price
#             context['persent'] = persent
#
#         return context

def Checkout(request):

    cart, created = Cart.objects.prefetch_related("item_set").get_or_create(user_id=request.user.id, status=True)
    items = cart.item_set.filter(product__status=True)
    items_false = cart.item_set.filter(product__status=False)
    items_false.delete()
    dicount = UserDiscountCode.objects.filter(cart_id=cart.id).first()

    if dicount is not None:
        discount_code = True
        persent = dicount.code.discount
        total_price = cart.total
        final_price = total_price - (total_price * (persent / Decimal('100')))
    else:
        discount_code = False
        final_price = cart.total
        persent = None


    userinfo = UserInfo.objects.filter(user_id=request.user.id , status=True).first()
    form = CheckoutForm(instance=userinfo)
    context = {
        'items':items,
        'cart':cart,
        'discount_code':discount_code,
        'persent':persent,
        'final_price' : final_price,
        'form':form
    }

    return render(request , 'dashboard_module/checkout.html' , context)


def Process_Order(request):

    data = request.GET
    final_price_js = data.get("total")
    cart = Cart.objects.filter(status=True , user_id=request.user.id).first()
    dicount = UserDiscountCode.objects.filter(cart_id=cart.id).first()
    if dicount is not None:
        persent = dicount.code.discount
        total_price = cart.total
        final_price = total_price - (total_price * (persent / Decimal('100')))
        cart.amount_paid = final_price
        cart.Independent_amount = cart.total
    else:
        final_price = cart.total
        cart.amount_paid = cart.total

    if float(final_price) == float(final_price_js):
        cart.status = False

    else:
        return JsonResponse({'status' : 'unsuccessful'})
    items = cart.item_set.all()
    for item in items:
        item.product.quantity = item.product.quantity - item.quantity
        item.final_price = item.product.selling_price
        item.save()
        item.product.save()
    cart.transection_id = data.get('transaction_id')
    cart.firstname = data.get('firstname')
    cart.lastname = data.get('lastname')
    cart.address = data.get('address')
    cart.zip = data.get('zip')
    cart.Country = data.get('country')
    cart.State = data.get('state')
    cart.save()
    return JsonResponse({'status':'successful'})

def RemoveProduct(request):

    if request.GET:

        item_id = request.GET.get("item_id")
        print(item_id)
        item = Item.objects.filter(id = item_id , cart__user_id=request.user.id , cart__status=True).first()
        if item is not None:
            item.delete()

            cart, created = Cart.objects.prefetch_related("item_set").get_or_create(user_id=request.user.id,status=True)
            items = cart.item_set.filter(product__status=True)
            items_false = cart.item_set.filter(product__status=False)
            items_false.delete()
            context = {
                'items': items,
                'cart': cart

            }
            cart_detail = render_to_string('dashboard_module/includes/cart_detail.html', context=context)

            return JsonResponse({'status':'deleted','cart_detail':cart_detail,'item_count':cart.item_count})
        else:
            return JsonResponse({"status": "NO"})
    else:
        return JsonResponse({"status":"NO"})



def CouponApply(request):

    data = request.POST
    print(data)
    discount_count = data.get("discount_code")
    print(discount_count)

    if request.user.is_authenticated:
        now = datetime.date.today()

        check_code = Discountcodes.objects.filter(code__exact=discount_count, status=True,valid_from__lte=now , valid_to__gte=now ).first()

        if check_code is not None:
            check_user = check_code.userdiscountcode_set.filter(code__code__exact=discount_count , cart__user_id=request.user.id ).first()
            if check_user is None:

                cart = Cart.objects.filter(status=True , user_id=request.user.id).first()
                persent = check_code.discount
                total_price = cart.total
                final_price = total_price - (total_price * (persent / Decimal('100')))
                final_price = format(final_price , '.2f')
                UserDiscountCode.objects.create(code_id=check_code.id , cart_id=cart.id)

                return JsonResponse({'status': "valid", 'persent':f'-{persent}%','final_price':final_price , 'total_price':total_price})
            else:
                return JsonResponse({'status' : "invalid"})

        else:
            return JsonResponse({'status': "invalid"})
    else:
        return JsonResponse({'status': "invalid"})



def ChangeCount(request):
    cart = Cart.objects.filter(user_id=request.user.id, status=True).first()
    if request.GET:
        status = request.GET.get('status')
        item_id = request.GET.get('item_id')
        item = Item.objects.filter(id=item_id ,cart_id=cart.id).first()
        if item is not None:
            if status == 'plus':
                quantity = item.quantity
                quantity_plus = quantity + 1
                if Product.objects.filter(id=item.product.id , status=True , quantity__gte=quantity_plus).exists():
                    item.quantity +=1
                    item.save()
                else:
                    return JsonResponse({'status': 'There is not enough stock'})
            else:
                quantity = item.quantity
                if quantity <= 1:
                    item.quantity=1
                    item.save()
                    return JsonResponse({'status': 'invalid'})
                else:
                    item.quantity -= 1
                    item.save()
    items = cart.item_set.filter(product__status=True)
    context = {
        'items': items,
        'cart': cart
    }
    cart_detail = render_to_string('dashboard_module/includes/cart_detail.html', context=context)
    return JsonResponse({'status':'successful' , 'html_code':cart_detail})



def Profile(request):
    # data = request.GET
    userinfo = UserInfo.objects.filter(user_id=request.user.id).first()
    count = Cart.objects.filter(status=False , user_id=request.user.id).count()
    # if data.get('profile_image'):
    #     avatar = data.get('profile_image')
    #
    #     userinfo.avatar = avatar
    #     print(avatar)
    #     userinfo.save()
    #     return JsonResponse({'status':'successful'})
    image_form = ImageForm()
    context = {
        'form':image_form,
        'userinfo':userinfo,
        'count':count
    }
    return render(request , 'dashboard_module/profile.html' , context)

def ChangeImgae(request):
    print(request.POST)
    userinfo = UserInfo.objects.filter(user_id=request.user.id).first()
    image = ImageForm(request.POST , request.FILES , instance=userinfo)
    if image.is_valid():
        print("ok")
        image.save()

    userinfo = UserInfo.objects.filter(user_id=request.user.id).first()
    count = Cart.objects.filter(status=False, user_id=request.user.id).count()
    image_form = ImageForm()
    context = {
        'form': image_form,
        'userinfo': userinfo,
        'count' : count
    }
    return render(request , 'dashboard_module/profile.html' , context)

def OrderHistory(request):
    carts = Cart.objects.filter(status=False , user_id=request.user.id)
    context = {
        'carts':carts
    }
    return render(request , 'dashboard_module/order_history.htm' , context)

# def OrderHistoryDetail(request):
#
#     return render(request , 'dashboard_module/order_history_detail.html')

def OrderHistoryDetail(request , pk):
    cart = Cart.objects.filter(user_id=request.user.id , pk = pk).first()
    context = {
        'object':cart
    }

    return render(request , 'dashboard_module/order_history_detail.html' , context)



def EditInformations(request):
    userinfo = UserInfo.objects.filter(user_id=request.user.id).first()
    form = CheckoutForm(instance=userinfo)
    context = {
        'form':form
    }

    if request.GET.get('zip'):
        data = request.GET
        userinfo.firstname = data.get('firstname')
        userinfo.lastname = data.get('lastname')
        userinfo.address = data.get('address')
        userinfo.zip = data.get('zip')
        userinfo.Country = data.get('country')
        userinfo.State = data.get('state')
        userinfo.save()
        html_c = render_to_string('dashboard_module/edit_informations.html' , context)
        return JsonResponse({'status':'successful' , 'html-code':html_c})
    else:
        return render(request , 'dashboard_module/edit_informations.html' , context)



