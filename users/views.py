from django.shortcuts import render, redirect
from django.contrib.auth.hashers import Argon2PasswordHasher
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import KhachHang, Customer
from . forms import FormDangKy, FormCustomer, FormUser
from cart.models import Order, OrderItem
from cart.cart import Cart


def login_signup(request):
    form = FormDangKy()
    result_signup = ''
    result_login = ''

    if request.POST.get('btnSignup'):
        form = FormDangKy(request.POST, KhachHang)
        if form.is_valid() and form.cleaned_data['mat_khau'] == form.cleaned_data['xac_nhan_mat_khau']:
            hasher = Argon2PasswordHasher()
            post = form.save(commit=False)
            post.ho = form.cleaned_data['ho']
            post.ten = form.cleaned_data['ten']
            post.dien_thoai = form.cleaned_data['dien_thoai']
            post.email = form.cleaned_data['email']
            # post.mat_khau = form.cleaned_data['mat_khau']
            post.mat_khau = hasher.encode(form.cleaned_data['mat_khau'], 'abcd@1234!')
            post.dia_chi = form.cleaned_data['dia_chi']
            post.save()
            result_signup = '''
                <div class="alert alert-success" role="alert">
                    Bạn đã đăng ký thành công, vui lòng đăng nhập để tiếp tục!!!
                </div>
            '''
        else:
            result_signup = '''
                <div class="alert alert-danger" role="alert">
                    Đăng ký không thành công, vui lòng kiểm tra dữ liệu nhập!
                </div>
            '''

    if request.POST.get('btnLogin'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        hasher = Argon2PasswordHasher()
        ma_hoa = hasher.encode(password, 'abcd@1234!')
        customer = KhachHang.objects.filter(email=email, mat_khau=ma_hoa)
        if customer.count() > 0:
            #tạo session
            request.session['s_customer'] = customer.values()[0]
            return redirect('store:index')
        else:
            result_login = '''
                <div class="alert alert-danger" role="alert">
                    Tên đăng nhập hoặc mật khẩu không đúng! Vui lòng thử lại
                </div>
            '''


    return render(request, 'users/login.html', {
        'form': form,
        'result_signup': result_signup,
        'result_login': result_login
    })


def user_logout(request):
    if 's_customer' in request.session:
        del request.session['s_customer']

    return redirect('user:login')


def login_signup2(request):
    result_signup = ''
    form_user = FormUser()
    form_customer = FormCustomer()
    if request.POST.get('btnSignup'):
        form_user = FormUser(request.POST)
        form_customer = FormCustomer(request.POST)
        if form_user.is_valid() and form_customer.is_valid():
            if form_user.cleaned_data['password'] == form_user.cleaned_data['confirm_password']:
                #User
                user = form_user.save()
                user.set_password(user.password)
                user.save()

                #Customer
                customer = form_customer.save(commit=False)
                customer.user = user
                customer.dien_thoai = form_customer.cleaned_data['dien_thoai']
                customer.dia_chi = form_customer.cleaned_data['dia_chi']
                customer.save()

                result_signup = '''
                    <div class="alert alert-success" role="alert">
                        Bạn đã đăng ký thành công, vui lòng đăng nhập để tiếp tục!!!
                    </div>
                '''
        else:
            result_signup = '''
                <div class="alert alert-danger" role="alert">
                    Đăng ký không thành công, vui lòng kiểm tra dữ liệu nhập!
                </div>
            '''

    # Đăng nhập
    if request.POST.get('btnLogin'):
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # if user is not None:
        if user:
            login(request, user)
            return redirect('store:index')


    return render(request, 'users/login2.html', {
        'form_user': form_user,
        'form_customer': form_customer,
        'result_signup': result_signup
    })


def user_logout2(request):
    logout(request)
    return redirect('user:login2')



def myaccount(request):
    if not request.user.username:
        return redirect('user:login2')

    result = ''

    if request.POST.get('btnUpdateUser'):
        ho = request.POST.get('last_name')
        ten= request.POST.get('first_name')
        dt = request.POST.get('mobile')
        dc = request.POST.get('address')

        s_customer = request.user
        customer = Customer.objects.get(user__id=s_customer.id)
        customer.user.last_name = ho
        customer.user.first_name = ten
        customer.dien_thoai = dt
        customer.dia_chi = dc
        customer.save()
        
        s_customer.last_name = ho
        s_customer.first_name = ten

        result = '''
            <div class="col-md-12">
                <div class="alert alert-success" role="alert">
                    Bạn đã cập nhật thành công!!!
                </div>
            </div>
            '''

    cart = Cart(request)
    orders = Order.objects.all()
    items = OrderItem.objects.all()    

    return render(request, 'users/my-account.html', {
        'result': result,
        'cart': cart,
        'orders': orders,
        'items': items
    })