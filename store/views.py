import requests
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator
from rest_framework import response, viewsets, permissions
from cart.cart import Cart
from . models import Category, SubCategory, Product, Contact
from . forms import FormContact
from . serializers import ProductSerializer
# from store.forms import FormContact


def index(request):
    cart = Cart(request)
    tbgd_subcategory = SubCategory.objects.filter(category__slug='thiet-bi-gia-dinh').values_list('slug')
    ddnb_subcategory = SubCategory.objects.filter(category__slug='do-dung-nha-bep').values_list('slug')

    tbgd_list_sub = []
    ddnb_list_sub = []

    for sub in tbgd_subcategory:
        tbgd_list_sub.append(sub[0])

    for sub in ddnb_subcategory:
        ddnb_list_sub.append(sub[0])

    tbgd_products = Product.objects.filter(subcategory__slug__in=tbgd_list_sub)
    ddnb_products = Product.objects.filter(subcategory__slug__in=ddnb_list_sub)

    # select * from store_product product, store_subcategory subcategory 
    # where product.subcategory_id=subcategory.id 
    # and subcategory.slug in ('ban-ui', 'cay-nuoc-nong-lanh', 
    # 'may-hut-bui', 'quat-dien', 'may-loc-nuoc')

    return render(request, 'store/index.html', {
        'tbgd_products': tbgd_products,
        'ddnb_products': ddnb_products,
        'cart': cart
    })


def productlist(request, slug):
    cart = Cart(request)
    sub_cats = SubCategory.objects.all()

    if slug == 'tat-ca-san-pham':
        products = Product.objects.all()
        sub_name = 'Tất cả sản phẩm (' + str(len(products)) + ')'
    else:
        products = Product.objects.filter(subcategory__slug=slug)
        select_sub = SubCategory.objects.get(slug=slug)
        sub_name = select_sub.name + ' (' + str(len(products)) + ')'

    #Lọc giá
    from_price = 0
    to_price = 0
    product_name = ''
    if request.GET.get('from_price'):
        from_price = int(request.GET.get('from_price'))
        to_price = int(request.GET.get('to_price'))
        product_name = request.GET.get('product_name')

        if product_name != '': # if product_name:
            products = Product.objects.filter(name__contains=product_name)
        products = [product for product in products if from_price <= product.price <= to_price] # list comprehension
        sub_name = f'Số sản phẩm có giá từ "{from_price}" đến "{to_price}": ' + '(' + str(len(products)) + ')'

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 20)
    products_pager = paginator.page(page)

    return render(request, 'store/product-list.html', {
        'sub_cats': sub_cats,
        'products': products_pager,
        'sub_name': sub_name,
        'to_price': to_price,
        'from_price': from_price,
        'product_name': product_name,
        'cart': cart
    })


def productdetail(request, pk):
    cart = Cart(request)
    product = Product.objects.get(pk=pk)
    sub_category_id = Product.objects.filter(pk=pk).values_list('subcategory')
    
    same_products = Product.objects.filter(subcategory__in=sub_category_id).exclude(pk=pk)

    sub_cats = SubCategory.objects.all()

    all_products = Product.objects.all()

    return render(request, 'store/product-detail.html', {
        'pk': pk,
        'product': product,
        'same_products': same_products,
        'sub_cats': sub_cats,
        'all_products': all_products,        
        'cart': cart
    })

def search(request):
    cart = Cart(request)
    product_name = ''
    if request.GET.get('product_search'):
        sub_cats = SubCategory.objects.all()
        product_name = request.GET.get('product_search')
        search_products = Product.objects.filter(name__contains=product_name)
        sub_name = f'Số sản phẩm có từ khóa "{product_name}": ' + '(' + str(len(search_products)) + ')'
    
    page = request.GET.get('page', 1)
    paginator = Paginator(search_products, 15)
    products_pager = paginator.page(page)

    return render(request, 'store/product-list.html', {
        'products': products_pager,
        'all_products': search_products,
        'product_name': product_name,
        'sub_cats': sub_cats,
        'sub_name': sub_name,
        'cart': cart
    })


def contact(request):
    cart = Cart(request)
    result = ''
    form = FormContact()
    if request.POST.get('btnSubmit'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()

            result = '''
                <div class="alert alert-success" role="alert">
                    Submit Successfully!!!
                </div>
            '''

    return render(request, 'store/contact.html', {
        'form': form,
        'result': result,
        'cart': cart
    })


# def demo_api(request):
#     url_api = "https://fakestoreapi.com/products/"
#     data = requests.get(url_api)

#     # return JsonResponse(data.text, safe=False)
#     return HttpResponse(data.text, content_type='application/json')


def api_update_product(request):
    url = requests.get("https://fakestoreapi.com/products/")
    items = url.json()
    if request.POST.get("btnSubmit"):
        for item in items:
            product = Product()
            product.subcategory = SubCategory.objects.get(pk=1)
            product.name = item.get("title")
            product.price = item.get("price")
            product.price_origin = item.get("price")
            product.content = item.get("description")
            product.image = item.get("image")
            product.viewed = item.get("rating").get("count")
            product.save()

    return render(request,'store/api_update.html')


def products_service(request):
    product = Product.objects.all()
    result_list = list(product.values('name', 'price', 'content', 'image'))

    return JsonResponse(result_list, safe=False)


def products_service_detail(request, pk):
    product = Product.objects.filter(pk=pk)
    result_list = list(product.values())[0]

    return JsonResponse(result_list, safe=False)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


