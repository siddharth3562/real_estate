from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.http import HttpResponse
import os


def e_login(req):
    if 'admin' in req.session:
        return redirect(admin_home)  
    if 'user' in req.session:
        return redirect(user_home) 
    
    if req.method == 'POST':
        uname = req.POST['uname']
        password = req.POST['password']
        user = authenticate(username=uname, password=password)

        if user:
            login(req, user)
            if user.is_superuser:
                req.session['admin'] = uname  # Set session for admin
                return redirect(admin_home)
            else:
                req.session['user'] = uname  # Set session for regular user
                return redirect(user_home)
        else:
            messages.warning(req, "Invalid username or password")
            return redirect(e_login)
    else:
        return render(req, 'login.html')

def user_reg(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        try:
            data=User.objects.create_user(first_name=uname,email=email,username=email,password=pswd)
            data.save()
        except:
            messages.warning(req, "email already in use")
            return redirect(user_reg)

        return redirect(e_login)
    else:
        return render(req,'reg.html')

def admin_home(req):
    if 'admin' not in req.session:
        return redirect(e_login)  
    return render(req, 'admin/home.html')

def admin_view_properties(request):
    if 'admin' not in request.session: 
        return redirect(e_login)  
    properties = Property.objects.all()
    return render(request, 'admin/view_property.html', {'properties': properties})

def approve_property(request, property_id):
    if 'admin' not in request.session:  
        return redirect(e_login)

    try:
        property_obj = Property.objects.get(id=property_id)  
    except Property.DoesNotExist:
        return HttpResponse("Property not found", status=404)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            property_obj.status = 'approved'
            property_obj.save()
            return redirect(admin_view_properties)
        elif action == 'reject':
            property_obj.status = 'rejected'
            property_obj.save()
            return redirect(admin_view_properties)

    return HttpResponse("Invalid request", status=400)

def list_user(req):
    if 'admin' in req.session:
        data=User.objects.all()
        return render(req,'admin/user_list.html',{'user':data})
    else:
        return redirect(e_login)

# user-------------------------------------------------------------------------------------------

def add_amenity(request):
    if 'user' not in request.session:
        return redirect('e_login')  
    
    user = User.objects.get(email=request.session['user'])  
    properties = Property.objects.filter(seller=user) 
    
    if request.method == 'POST':
        property_id = request.POST.get('property')  
        amenity_name = request.POST.get('name')  
        
        property_obj = Property.objects.get(id=property_id)
        
        Amenities.objects.create(
            name=amenity_name,
            property=property_obj
        )
        return redirect(add_amenity)  
    user_amenities = Amenities.objects.filter(property__seller=user)
    return render(request, 'user/add_amenity.html', {
        'properties': properties,
        'user_amenities': user_amenities
    })

    
def user_home(req):
    if 'user' not in req.session:
        return redirect(e_login)

    properties = Property.objects.filter(status='approved').exclude(seller=req.user).order_by('-id')[:4]

    return render(req, 'user/home.html', {'properties': properties})

def buy_page(req):
    if 'user' not in req.session:
        return redirect(e_login)
    properties = Property.objects.filter(status='approved',availability='For Sale').exclude(seller=req.user).order_by('-id')[:4]

    return render(req, 'user/buy.html', {'properties': properties})

def rent_page(req):
    if 'user' not in req.session:
        return redirect(e_login)
    properties = Property.objects.filter(status='approved',availability='For Rent').exclude(seller=req.user).order_by('-id')[:4]

    return render(req, 'user/rent.html', {'properties': properties})


def property_detail(req, property_id):
    if 'user' not in req.session:
        return redirect(e_login)

    try:
        property = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        return redirect(user_home)  # Redirect if the property doesn't exist

    seller_name = property.seller.get_full_name() 
    amenities = Amenities.objects.filter(property=property)

    return render(req, 'user/property_details.html', {
        'property': property,
        'seller_name': seller_name,
        'amenities': amenities,

    })


def add_property(req):
    if 'user' not in req.session:
        return redirect('e_login')

    if req.method == 'POST':
        title = req.POST.get('title')
        description = req.POST.get('description')
        price = req.POST.get('price')
        property_type = req.POST.get('property_type')
        address = req.POST.get('address')
        city = req.POST.get('city')
        state = req.POST.get('state')
        bedrooms = req.POST.get('bedrooms')
        bathrooms = req.POST.get('bathrooms')
        area = req.POST.get('area')
        availability = req.POST.get('availability')
        image1 = req.FILES.get('image1')
        image2 = req.FILES.get('image2')
        image3 = req.FILES.get('image3')

        seller = User.objects.get(username=req.session['user'])  
        Property.objects.create(
            title=title,
            description=description,
            price=price,
            property_type=property_type,
            address=address,
            city=city,
            state=state,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area=area,
            availability=availability,
            seller=seller,
            image1=image1,
            image2=image2,
            image3=image3,
        )

        messages.success(req, 'Your property has been submitted successfully. Please wait for admin approval.')

        return redirect(add_amenity)  

    return render(req, 'user/sell_property.html')

def user_view_properties(request):
    if 'user' not in request.session:
        return redirect('e_login')  

    user = User.objects.get(username=request.session['user'])
    user_properties = Property.objects.filter(seller=user)

    return render(request, 'user/view_property.html', {'properties': user_properties})
    

def edit_property(request, property_id):
    if 'user' not in request.session:
        return redirect(e_login) 
    
    try:
        property = Property.objects.get(id=property_id, seller__username=request.session['user'])
    except Property.DoesNotExist:
        return redirect(user_view_properties)  

    if request.method == 'POST':
        property.title = request.POST.get('title')
        property.description = request.POST.get('description')
        property.price = request.POST.get('price')
        property.property_type = request.POST.get('property_type')
        property.address = request.POST.get('address')
        property.city = request.POST.get('city')
        property.state = request.POST.get('state')
        property.bedrooms = request.POST.get('bedrooms')
        property.bathrooms = request.POST.get('bathrooms')
        property.area = request.POST.get('area')
        property.availability = request.POST.get('availability')

        # Handle image1 update
        img1 = request.FILES.get('image1')
        if img1:
            if property.image1:
                old_img_path = property.image1.path
                if os.path.isfile(old_img_path):
                    os.remove(old_img_path)
            property.image1 = img1

        # Handle image2 update
        img2 = request.FILES.get('image2')
        if img2:
            if property.image2:
                old_img_path = property.image2.path
                if os.path.isfile(old_img_path):
                    os.remove(old_img_path)
            property.image2 = img2

        # Handle image3 update
        img3 = request.FILES.get('image3')
        if img3:
            if property.image3:
                old_img_path = property.image3.path
                if os.path.isfile(old_img_path):
                    os.remove(old_img_path)
            property.image3 = img3

        property.save()
        return redirect(user_view_properties)
    
    return render(request, 'user/edit_property.html', {'property': property})

    
def e_logout(req):
    logout(req)
    req.session.flush()
    return redirect(e_login)


def delete_property(request, property_id):
    if 'user' not in request.session:
        return redirect(e_login)  
    try:
        property = Property.objects.get(id=property_id, seller__username=request.session['user'])
    except Property.DoesNotExist:
        return redirect(user_view_properties) 
    if request.method == 'POST':
        if property.image1 and os.path.isfile(property.image1.path):
            os.remove(property.image1.path)
        if property.image2 and os.path.isfile(property.image2.path):
            os.remove(property.image2.path)
        if property.image3 and os.path.isfile(property.image3.path):
            os.remove(property.image3.path)
        property.delete()
        return redirect(user_view_properties)  
    return redirect(user_view_properties)

def property_search(request):
    availability = request.GET.get('availability')
    property_type = request.GET.get('property_type')
    city = request.GET.get('location') 

    properties = Property.objects.all()

    if availability:
        properties = properties.filter(availability=availability)
    if property_type:
        properties = properties.filter(property_type=property_type)
    if city:
        properties = properties.filter(city__icontains=city)  # Match partial city name

    return render(request, 'user/property_list.html', {'properties': properties})


def contact_seller_view(request, property_id):
    property = Property.objects.get(id=property_id)
    seller = property.seller  # Assuming there's a 'seller' field in the Property model
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        if name and email and phone_number:
            # Create and save the ContactSeller object
            ContactSeller.objects.create(
                property=property,
                name=name,
                email=email,
                phone_number=phone_number,
                receiver=seller  # Set the receiver as the seller of the property
            )
            # Redirect to a success page or show a success message
            return redirect(success_page)  # Provide property_id
    
    return render(request, 'user/contact.html', {'property': property})

def success_page(request):
    return render(request, 'user/success.html')

def seller_contact_messages(request):
    seller = request.user 
    properties = Property.objects.filter(seller=seller)
    
    contact_messages = ContactSeller.objects.filter(property__in=properties)

    return render(request, 'user/messages.html', {'contact_messages': contact_messages})