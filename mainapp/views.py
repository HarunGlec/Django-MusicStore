from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from models import Product,Inventory,Cart,Users,User,Type_of_Product
from mainapp.forms import RegistrationForm,AddProductForm
from django.contrib import messages
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response

def index(request):
	if request.user.is_authenticated():
		user=Users.objects.get(id=request.user.id)
		manager=user.manager
	else:
		manager=False
	return render(request,'index.html',{ 'manager' : manager})
    
@login_required()
def store(request):
	user=Users.objects.get(id=request.user.id)
	manager=user.manager
	items=Inventory.objects.all()
	return render(request,'store.html',{ 'items' : items,'manager' : manager })
    
@login_required()
def cart(request):
	user=Users.objects.get(id=request.user.id)
	manager=user.manager
	cart=Cart.objects.filter(users_id__user=request.user).order_by('status')
	return render(request,'cart.html',{ 'cart' : cart,'manager' : manager })

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            users=Users.objects.get(user=user)
            users.manager=form.cleaned_data['manager']
            users.save()
            return HttpResponseRedirect('/mainapp/')
    else:
		user=Users.objects.get(id=request.user.id)
		manager=user.manager
		form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form,
    'manager' : manager
    })
 
    return render_to_response(
    'register.html',
    variables,
    )
        
def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'logout.html')
    
@login_required()
def addToCart(request):
	item = get_object_or_404(Inventory, pk=request.POST['item_id'])
	user=Users.objects.get(id=request.user.id)
	cart=Cart(quantity=1, boughtPrice=item.product_id.price,product_id=item.product_id,users_id=user)
	cart.save()
	item.quantity=item.quantity-1
	item.save()
	return HttpResponse(user)

@login_required()
def deleteFromCart(request):
	item = get_object_or_404(Cart, pk=request.POST['item_id'])
	if not item.status:
		item.delete()
	return HttpResponse(True)

@login_required()
def manager(request):
	return render(request,'manager.html')

@login_required()		
def product(request):
	products=Inventory.objects.filter(product_id__manager_id=request.user.id)	
	return render(request,'product.html',{'items':products})

@csrf_protect	
def addProduct(request):
	if request.method == 'POST':
		form = AddProductForm(request.POST)
		if form.is_valid():
			cat=Type_of_Product.objects.get(id=form.cleaned_data['category'])
			product = Product.objects.create(
			name=form.cleaned_data['name'],
			price=form.cleaned_data['price'],
			category=cat,
			manager_id=Users.objects.get(user=request.user)
			)
			inventory=Inventory.objects.create(product_id=product,quantity=form.cleaned_data['quantity'])
			return HttpResponseRedirect('/mainapp/product')
	else:
		form = AddProductForm()
		variables = RequestContext(request, {'form': form})
		return render_to_response('add.html',variables)

@csrf_protect
def deleteProduct(request):
	i=get_object_or_404(Inventory, pk=request.POST['item_id'])
	item = get_object_or_404(Product, pk=i.product_id.id)
	item.delete()
	return render_to_response('product.html')	

def updateProduct(request,item_id):
	if request.method == 'POST':
		form = AddProductForm(request.POST)
		if form.is_valid():
			cat=Type_of_Product.objects.get(id=form.cleaned_data['category'])
			i=get_object_or_404(Inventory, pk=item_id)
			p=get_object_or_404(Product, pk=i.product_id.id)
			p.name=form.cleaned_data['name']
			p.price=form.cleaned_data['price']
			p.category=cat
			p.save()
			i.quantity=form.cleaned_data['quantity']
			i.save()
			return HttpResponseRedirect('/mainapp/product')
	else:
		item=get_object_or_404(Inventory, pk=item_id)
		form = AddProductForm(initial={'name': item.product_id.name,'price':item.product_id.price,'quantity':item.quantity,'category':item.product_id.category.id})
		variables = RequestContext(request, {'form': form})
		return render_to_response('updateProduct.html',variables)	
	
def confirm(request):
	if request.method == 'POST':
		item=item = get_object_or_404(Cart, pk=request.POST['item_id'])
		item.status=True
		item.save()
		return HttpResponse(True)
	else:
		cart=Cart.objects.filter(product_id__manager_id__user=request.user)
		return render(request,'confirm.html',{'items':cart})
		