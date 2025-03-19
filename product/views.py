from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product,Review
from .serializers import ProductSerializer
from .filters import ProductsFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Avg 
# Create your views here.



@api_view(['GET'])
def get_all_products(request):
    filterset=ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count=filterset.qs.count()
    resPage=900 # controls how many products appear on one page
    paginator=PageNumberPagination() 
    paginator.page_size = resPage
    queryset=paginator.paginate_queryset(filterset.qs,request)
    
    ##products = Product.objects.all()
    ##serializer=ProductSerializer(products,many=True)
    ###serializer=ProductSerializer(filterset.qs,many=True)
    
    serializer=ProductSerializer(queryset,many=True)
    
    
    return Response({"products":serializer.data,"per page":resPage,"count":count})


  
  
  
  
  
  
  
@api_view(['GET'])
def get_by_id_product(request,pk):
    products = get_object_or_404(Product,id=pk) #if the object is present, bring it, if not, error 404
    serializer=ProductSerializer(products,many=False)
     
    return Response({"product":serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data=request.data
    serializer=ProductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data,user=request.user)
        res= ProductSerializer(product,many=False)
     
        return Response({"Created product":res.data})
    else:
        return Response (serializer.errors)
    
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    if product.user != request.user:
        return Response({"Error":"Access Deniedddd"},status=status.HTTP_403_FORBIDDEN)
    product.name= request.data['name']
    product.desc=request.data['desc']
    product.price=request.data['price']
    product.brand=request.data['brand']
    product.category=request.data['category']
    product.ratings=request.data['ratings']
    product.stock=request.data['stock']    
    product.save()
    serializer= ProductSerializer(product,many=False)
    return Response({"product":serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    if product.user != request.user:
        return Response({"Error":"Access Deniedddd"},status=status.HTTP_403_FORBIDDEN) 
    product.delete()
    return Response({"Action":"Succesfully Deleted"},status=status.HTTP_200_OK)
    
        
    




# In Django REST Framework (DRF), pagination is used to control how many objects are sent back in a single API response. This is especially useful when you have a large dataset and don't want to return all the data in one response. Pagination breaks down the dataset into smaller "pages."

# PageNumberPagination: This is one of the pagination classes provided by DRF. It allows users to specify which page of results they want by using a query parameter (usually page).

# paginator.page_size: This sets the number of items to be displayed per page. In your code, resPage = 2 means that each page will contain 2 items.
  
#views.py
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)
    data=request.data
    review=product.reviews.filter(user=user) #from related_name = reviews in Review Class

    if data['rating']<=0 or data['rating'] >10:
      return Response({"error":"Rating out of range, (1->10)"},status=status.HTTP_400_BAD_REQUEST)      
    elif review.exists():
        new_review={'rating':data['rating'],'comment':data['comment']}
        review.update(**new_review)
        
        rating=product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.ratings=rating['avg_ratings']
        product.save()
        
        return Response({'details':'Product review updated'})
    else:
        Review.objects.create(
            user=user,
            product=product,
            rating=data['rating'],
            comment=data['comment']
        )
        rating=product.reviews.aggregate(avg_ratings=Avg('rating'))
        product.ratings=rating['avg_ratings']
        product.save()
        return Response({'details':'Product review updated'})
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    user=request.user
    product=get_object_or_404(Product,id=pk)
    
    review=product.reviews.filter(user=user)
    
    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_ratings=Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg ratings']= 0
        product.ratings=rating['avg_ratings']
        product.save()
        return Response({'details':"Review Deleted"})
    else:
        return Response({'details':"Review not found"},status=status.HTTP_404_NOT_FOUND)
        

    