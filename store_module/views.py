from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from dashboard_module.models import Cart, UserInfo, Item, Comment
from utils.group_list import Group_list
from utils.User_IP_Service import Get_Client_IP
# Create your views here.
from django.views.generic import ListView, DetailView

from store_module.models import Slider, Product, Category, ProductImageGallery, ProductView, Comments


def Home(request):
    sliders = Slider.objects.filter(status=True)
    best_seller_product = Product.objects.filter(item__cart__status=False).annotate(product_count=Sum('item__quantity')).order_by('-product_count')[:12]
    best_seller_product = Group_list(best_seller_product)
    most_view = Product.objects.filter(status=True).annotate(view = Count('productview')).order_by('-view')[:12]
    most_view = Group_list(most_view)
    new_products = Product.objects.filter(status=True).order_by('-created_at')[:12]
    new_products = Group_list(new_products)
    context = {
        'sliders' : sliders,
        'best_seller_product':best_seller_product,
        'most_view':most_view,
        'new_products':new_products
    }
    return render(request, 'store_module/index.html', context=context)





def ProductList(request , category):
    get_category = Category.objects.filter(slug=category).first()
    if get_category is None:
        print("ok")
        return

    product_list = Product.objects.filter(status=True , category__slug=category)
    if request.GET:
        data = request.GET.get('filter_type')
        if data == 'most_e':
            product_list = product_list.order_by('-selling_price')
        elif data == 'cheapest':
            product_list = product_list.order_by('selling_price')
    paginator = Paginator(product_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    object_list = Group_list(page_obj.object_list)

    context = {
        'page_obj':page_obj,
        'product_list':object_list,
        'paginator':paginator,
        'category':get_category
    }
    return render(request , 'store_module/product_list.html' , context)







def ProductCategory(request):
    category_id = request.GET.get('category_id')
    category = Category.objects.filter(id=category_id).first()
    if category is None:
        return JsonResponse({'status' : 'unsuccessful'})
    products = Product.objects.filter(status=True , category__id = category_id)[:16]

    product_list = Group_list(products)
    if product_list == []:
        status = "unsuccessful"
    else:
        status = 'successful'

    context = {
        'product_list' :product_list,
        'category': category
    }

    product_html = render_to_string('store_module/includes/product_item.html',context)
    return JsonResponse({'status':status , 'product_html':product_html , 'category':category.name})



class ProductDetail(DetailView):
    template_name = 'store_module/product_detail.html'
    model = Product

    def get_queryset(self):
        query = super(ProductDetail, self).get_queryset()
        query = query.filter(status = True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        category = self.object.category.filter(status = True).exclude(parent=None).first()
        context['category'] = category
        imagegallery = ProductImageGallery.objects.filter(status=True , product_id=self.object.id)[:5]
        context['imagegallery'] = imagegallery
        product_id = self.object.id
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        else:
            user_id = None
        user_ip = Get_Client_IP(self.request)
        check_user = ProductView.objects.filter(user_ip__iexact=user_ip, product_id=product_id).exists()
        if not check_user:
            ProductView.objects.create(product_id=product_id, user_ip=user_ip, user_id=user_id)
        related_products =  Product.objects.filter(status=True , category=category).exclude(id=self.object.id)[:12]
        related_products = Group_list(related_products)
        context['related_products'] = related_products

        comments = Comment.objects.filter(product_id=self.object.id).order_by('-date')
        context['comments'] = comments
        context['comments_count'] = comments.count()
        return context


def Addcomment(request):
    print("ok")
    text = request.GET.get('text')
    product_id = request.GET.get('product_id')

    product = Product.objects.filter(status=True , id=product_id).first()
    if product is not None:
        user_info = UserInfo.objects.filter(user_id=request.user.id).first()
        Comment.objects.create(product_id=product_id , user_id=request.user.id , userinfo_id=user_info.id , text=text)
        comments = Comment.objects.filter(product_id=product_id).order_by('-date')
        context = {
            'comments':comments,
        }
        html_code = render_to_string('store_module/includes/comment_box.html' , context=context)
        return JsonResponse({'status':'successful' , 'html_code':html_code ,'count':f"Comments ({comments.count()})"})
    return JsonResponse({'status':'unsuccessful'})



def search(request):

    product = Product.objects.filter(status=True).values_list('name', flat=True)
    productlist = list(product)
    return JsonResponse({'product_list':productlist})


def ShowResult(request):
    product = Product.objects.filter(status=True , name__icontains=request.GET.get('text'))
    if product.count() == 1:
        product = product.first()
        return JsonResponse({'status':'one' , 'slug':product.slug})

    elif product.count() >1:
        product_list = Group_list(product)
        context = {
            'product_list': product_list,
        }
        product_html = render_to_string('store_module/includes/product_item.html',context)
        return JsonResponse({'status':'more' , 'product_html':product_html})
    else:
        return JsonResponse({'status':'not found'})




def Menu(request):
    main_category = Category.objects.prefetch_related('category_set','product_set').filter(status=True,parent=None)
    context = {
        'main_categorys':main_category
    }
    return render(request , 'store_module/includes/menu.html' , context)



def Navbar(request):
    if request.user.is_authenticated:
        userinfo = UserInfo.objects.filter(user_id=request.user.id).first()
        cart , created = Cart.objects.get_or_create(status=True , user_id=request.user.id)
        count = cart.item_set.filter(product__status=True).count()
    else:
        count = 0
        userinfo = None
    context = {
        'count':count,
        'userinfo':userinfo
    }
    return render(request , 'shared/includes/navbar.html',context)







def Footer(request):
    return render(request , 'shared/includes/footer.html')