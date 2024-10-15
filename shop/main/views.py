from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404

from .models import Product, User, Order, LikedProduct
from .forms import ProductForm
from django.views.generic.edit import UpdateView


def index(request):
    products = Product.objects.all()
    return render(request,
                  'main/index.html',
                  {'products': products}
                  )

def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404("No Product exist")
    return render(
        request,
        'main/index/detail.html',
        {'product' : product }
    )

def about(request):

    return render(request, 'main/about.html')

def busket(request):
    orders = Order.objects.all()
    return render(request, 'main/busket.html', {'orders':orders})

def sign_in(request):
    return render(request, 'main/sign_in.html')

def add_product(request):
    error=''
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            form.save()
            return redirect('home')
        else:
            error="u r doing it wrong"

    form = ProductForm()

    context={
        'form': form,
        'error' : error
    }

    return render(request, 'main/add_product.html', context)

def like_product(request):

    if request.method == 'POST':
        liked_product = LikedProduct("product"=product[id], 'user'=request_user )
        return HttpResponse("hi")





    return render(request, 'main/index.html')



def make_order(request):
    error=''
    if  request.method== 'POST':
        form = OrderForm(request.POST)

        return redirect('busket')

    context = {
        'form' : form,
        'error' : error
    }

    return render(request, 'main/index.html', context)

"""
def order_product(request):
    product = Product.objects.get(id=id)
    order = Order(
        title = product.title,
        price = product.price

    )
    return render(request, 'main/order_product.html')
"""
"""

def make_order(request):
    #response = "You're looking at %s."
    #return HttpResponse(response % product_id)
    product = Product.objects.get(id=id)

    new_order = Order(
        title=product.title
    )


    #return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
"""
"""
def get_urls(request):

    return render(request, 'main/make_order/<int:product.id>')
"""
"""
def order_product(self, request):
    self.model.objects.all().update(status = 'PAID')
    return HttpResponseRedirect("../")
"""