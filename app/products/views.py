# products/views.py
from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Contact,CartItem,Wishlist 
from django.core.paginator import Paginator
from django.db.models import Q
from category.models import Category
from django.http import JsonResponse

def home(request):
    products = Product.objects.filter(is_available=True).prefetch_related('details_image')
    categories = Category.objects.all()

    deals = []
    for product in products:
        discount = product.discount_percent()
        if discount > 5:
            deals.append(product)
    featured = products.order_by('-reviews')[:8]
    new_arrivals = products.order_by('-created_date')[:6]
    return render(request, 'ecommerce/home.html', 
                    {'products': products, 
                    'deals' : deals , 
                    'categories': categories ,
                    'featured' : featured ,
                    'new_arrivals' : new_arrivals ,
                    })

  

def all_products(request):

    query = request.GET.get('z' , '' )   
    category_id = request.GET.get("category")
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(product_name__icontains=query) | 
            Q(category__cat_name__icontains=query)
        )

    categories = Category.objects.all()

    category = request.GET.getlist('category')  
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    availability = request.GET.get('is_available')

    if category:
        products = products.filter(category__id__in = category)

    if min_price:
        try:
            products = products.filter(original_price__gte = int(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(original_price__lte = int(max_price))
        except ValueError:
            pass

    if availability:
        if 'in' in availability and 'out' not in availability:
            products = products.filter(is_available = True)
        elif 'out' in availability and 'in' not in availability:
            products = products.filter(is_available = False)

    products = products.prefetch_related('details_image')

    sort = request.GET.get('sort')
    view = request.GET.get('view' , 'grid')
    selected_sort = "Popularity"

    if sort== 'price_low':
        products = products.order_by('discount_price')
        selected_sort = "Price Low to High"
    elif sort== 'price_high':
        products = products.order_by('-discount_price')
        selected_sort = "Price High to Low"
    elif sort== 'newest':
        products = products.order_by('-created_date')
        selected_sort = 'Newest First'
    
    is_deals = request.GET.get('deals') == 'true'
    is_new = request.GET.get('new') == 'true'
    if is_deals:
        filtered_deals = []
        for product in products:
            if product.discount_percent() > 5:
                filtered_deals.append(product)
        products = filtered_deals
        heading = "Deals of the Day"
    elif is_new:
        products = products.order_by('-created_date')
        heading = "New Arrivals"
    else:
        heading = "All Products"

    paginator = Paginator(products , 6)    # 10 products per page
    page_number = request.GET.get('page')   # current page number
    page_object = paginator.get_page(page_number)   # display 10 products on current page


    selected_category = Category.objects.filter(id = category_id).first()
    if selected_category:
        selected_category = selected_category.cat_name
    else:
        selected_category = 'all products'

    context = {
        'page_object': page_object , 
        'categories' : categories ,
        'selected_categories' : category , 
        'selected_min_price' : min_price or 0 ,
        'selected_max_price' : max_price or 10000000 ,
        'selected_availability' : availability,
        'selected_sort' : selected_sort ,
        'view' : view ,
        'request' : request , 
        'heading' : heading,
        'search_query' : query ,
        'selected_category' : selected_category ,
        }

    return render(request, 'products/all_products.html', context)



def contact(request):
    if request.method == 'POST':
        name_var=request.POST.get('name')
        contact_var = request.POST.get('contact')
        email_var= request.POST.get('email')
        description_var = request.POST.get('description')


        cont = Contact(
            name = name_var,
            email = email_var,
            contact = contact_var,
            description = description_var
        )
        cont.save()
        return redirect ('home')
    return render(request, 'ecommerce/contact.html')  




def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    image = product.details_image.all()
    valid_colors = []
    for img in image:
        if img.colors and img.colors.lower() != "none":
            valid_colors.append(img)
    return render(request, 'products/product_details.html', {'product': product , 'valid_colors' : valid_colors})


def cart(request):                        

    cart_id = request.session.get('register_id')   

    if not cart_id:
        return redirect('login') 
    
    items = CartItem.objects.filter(user_id = cart_id)

    total = 0   # total amnt user has to pay
    discount = 0    # total discount
    total_quantity = 0  

    for item in items:
        item_total = item.total_price()     # price of each product
        item_discount = item.discount_price()
        
        item.line_total = item_total
        item.line_original_total = item.product.original_price * item.quantity
        item.line_discount = item_discount

        total += item_total
        discount += item_discount
        total_quantity += item.quantity

    if total>=2000 or total==0:
        shipping = 0
    else:
        shipping = 199

    grand = total + shipping
    return render(request , 'cart/cart.html' , {
        'items' : items , 
        'total' : total , 
        'discount' : discount ,
        'grand' : grand,
        'total_quantity' : total_quantity,
        'shipping' : shipping
        })

def add_to_cart(request , product_id):
    register_id = request.session.get('register_id')
    if not register_id:
        return redirect('login')
    product = get_object_or_404(Product, id= product_id) 

    # Use register_id, not request.user
    cart, created = CartItem.objects.get_or_create(user_id=register_id, product=product)
    if not created:
        cart.quantity += 1
        cart.save() 

    return redirect('cart')
def delete_from_cart(request , item_id):
    
    proj = get_object_or_404(CartItem, id = item_id,) 
    proj.delete()
    return redirect('cart')  

#quantity increase
def increase(request , item_id):
    product = get_object_or_404(CartItem , id = item_id)
    product.quantity += 1
    product.save()
    return redirect('cart')
#quantity decrease
def decrease(request , item_id):
    item = get_object_or_404(CartItem , id=item_id)
    if item.quantity <= 1 :
        item.delete()
    else:
        item.quantity -= 1
        item.save()
    return redirect('cart')    




#wishlist
def wishlist(request):
    wishlist_id = request.session.get('register_id')   

    if not wishlist_id:
        return redirect('login') 
    
    items = Wishlist.objects.filter(user_id = wishlist_id)  

    return render(request,'accounts/wishlist.html' , {'items':items })
   

def add_to_wishlist(request,product_id):
    wishlist_id =request.session.get('register_id')
    if not wishlist_id:
        return redirect('login')
    product = get_object_or_404(Product , id = product_id)

    wishlist = Wishlist.objects.filter(user_id = wishlist_id,product = product).first()

    if not wishlist:
        Wishlist.objects.create(
            user_id = wishlist_id,
            product = product)
        return JsonResponse({'status' : 'added'})
    else:
        wishlist.delete()
        return JsonResponse({'status' : 'deleted'})

def delete_from_wishlist(request , product_id):
    user_id = request.session.get('register_id')
    wishlist = get_object_or_404(Wishlist, product_id = product_id , user_id = user_id)
    wishlist.delete()
    return redirect('wishlist')
   

def buy_now(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id") 
        product = get_object_or_404(Product , id = product_id)

        request.session['buy_now_product'] = {
            'id' : product.id , 
            'quantity' : 1
        }

        return redirect('address')

    return redirect('all_products')


def about(request):
    return render(request, 'ecommerce/about.html')

def help_center(request):
    return render(request , 'ecommerce/help_center.html')

def terms_conditions(request):
    return render(request,'ecommerce/terms_conditions.html')    