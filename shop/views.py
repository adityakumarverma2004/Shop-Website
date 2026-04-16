from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Category, ContactMessage

def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:6]
    return render(request, 'shop/index.html', {'featured_products': featured_products})

def gallery(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    category_slug = request.GET.get('category')
    min_price_str = request.GET.get('min_price')
    max_price_str = request.GET.get('max_price')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
        
    # Get highest and lowest price dynamically from DB
    from django.db.models import Max, Min
    price_aggs = Product.objects.aggregate(Max('price'), Min('price'))
    highest_price = int(price_aggs['price__max']) if price_aggs['price__max'] else 1000000
    lowest_price = int(price_aggs['price__min']) if price_aggs['price__min'] else 0

    current_max_price = highest_price
    
    if max_price_str:
        try:
            current_max_price = float(max_price_str)
            products = products.filter(price__lte=current_max_price)
            current_max_price = int(current_max_price)
        except ValueError:
            pass
            
    if min_price_str:
        try:
            min_price = float(min_price_str)
            products = products.filter(price__gte=min_price)
        except ValueError:
            pass

    context = {
        'categories': categories,
        'products': products,
        'selected_category': category_slug,
        'highest_price': highest_price,
        'lowest_price': lowest_price,
        'current_max_price': current_max_price
    }
    return render(request, 'shop/gallery.html', context)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        if name and phone and message:
            ContactMessage.objects.create(
                name=name, phone=phone, message=message
            )
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')
            
    return render(request, 'shop/contact.html')

from django.shortcuts import get_object_or_404

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Get other related products from same category to show at bottom
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/product_detail.html', context)

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import ProductImage

@staff_member_required
def delete_product_image_ajax(request, image_id):
    if request.method == 'POST':
        try:
            image = ProductImage.objects.get(id=image_id)
            image.delete()
            return JsonResponse({'success': True})
        except ProductImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})
