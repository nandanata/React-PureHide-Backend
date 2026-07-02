from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework import generics
from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import 
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .models import Product
from .serializers import  WishlistSerializer
from .serializers import ProductCardSerializer
from .serializers import DuffleCardSerializer
from .serializers import BriefCardSerializer
from .serializers import CrossCardSerializer
from .serializers import MenWalletCardSerializer
from .serializers import MenBeltCardSerializer
from .serializers import MenShoeCardSerializer
from .serializers import MenChelseaCardSerializer
from .serializers import MenDesertCardSerializer
from .serializers import WomenHandBagCardSerializer
from .serializers import WomenToteBagCardSerializer
from .serializers import WomenSlingBagCardSerializer
from .serializers import WomenTrBagCardSerializer
from .serializers import WomenWalletCardSerializer
from .serializers import WomenBeltCardSerializer
from .serializers import WomenFlipCardSerializer
from .serializers import WomenSandalCardSerializer
from .serializers import WomenLoaferCardSerializer
from .serializers import KidsTravelCardSerializer
from .serializers import  KidsBackPackCardSerializer
from .serializers import KidsDiaperBagCardSerializer
from .serializers import  KidsBagcharmCardSerializer
from .serializers import KidShoeCardSerializer
from .serializers import KidChelCardSerializer
from .serializers import KidDesCardSerializer
from .models import (
    GenderCategory,
    ProductType,
    SubCategory,
    Color,
    Product,
    ProductVariant,
    ProductImage,
    CustomUser
    
)

from .serializers import (
    GenderCategorySerializer,
    ProductTypeSerializer,
    SubCategorySerializer,
    ColorSerializer,
    ProductSerializer,
    ProductVariantSerializer,
    ProductImageSerializer,
    RegisterSerializer,
    LoginSerializer

)


# -----------------------------------
# GENDER CATEGORY
# -----------------------------------

class GenderCategoryListCreateView(
    generics.ListCreateAPIView
):

    queryset = GenderCategory.objects.all()

    serializer_class = GenderCategorySerializer


class GenderCategoryDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = GenderCategory.objects.all()

    serializer_class = GenderCategorySerializer




# -----------------------------------
# PRODUCT TYPE
# -----------------------------------

class ProductTypeListCreateView(
    generics.ListCreateAPIView
):

    queryset = ProductType.objects.all()

    serializer_class = ProductTypeSerializer



class ProductTypeDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = ProductType.objects.all()

    serializer_class = ProductTypeSerializer





# -----------------------------------
# SUBCATEGORY
# -----------------------------------

class SubCategoryListCreateView(
    generics.ListCreateAPIView
):

    queryset = SubCategory.objects.all()

    serializer_class = SubCategorySerializer


class SubCategoryDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = SubCategory.objects.all()

    serializer_class = SubCategorySerializer





class ColorListCreateView(
    generics.ListCreateAPIView
):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class ColorDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer





## View all products + Create product
class ProductListCreateView(
    generics.ListCreateAPIView
):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer


# View one product + Update + Delete
class ProductDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer



# -----------------------------------
# PRODUCT DETAIL
# -----------------------------------

class ProductDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = Product.objects.all()

    serializer_class = ProductSerializer


# -----------------------------------
# PRODUCT VARIANT
# -----------------------------------

# CREATE + VIEW ALL
class ProductVariantListCreateView(
    generics.ListCreateAPIView
):

    queryset = ProductVariant.objects.all()

    serializer_class = ProductVariantSerializer



# VIEW ONE + UPDATE + DELETE
class ProductVariantDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = ProductVariant.objects.all()

    serializer_class = ProductVariantSerializer

# -----------------------------------
# PRODUCT IMAGE
# -----------------------------------
# CREATE + VIEW ALL
class ProductImageListCreateView(
    generics.ListCreateAPIView
):

    queryset = ProductImage.objects.all()

    serializer_class = ProductImageSerializer




# VIEW ONE + UPDATE + DELETE
class ProductImageDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = ProductImage.objects.all()

    serializer_class = ProductImageSerializer



# USER DETAIL VIEW
# -----------------------------------

class UserDetailView(
    generics.RetrieveAPIView
):

    queryset = CustomUser.objects.all()

    serializer_class = RegisterSerializer




class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            return Response(

                {
                    "message": "Login successful",
                    "username": serializer.validated_data["username"]
                },

                status=status.HTTP_200_OK
            )

        return Response(

            serializer.errors,

            status=status.HTTP_400_BAD_REQUEST
        )



class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "User registered successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

# -----------------------------------
# LOGOUT VIEW
# -----------------------------------

class LogoutView(APIView):

    def post(self, request):

        logout(request)

        return Response(

            {
                "message": "Logout successful"
            },

            status=status.HTTP_200_OK
        )
    

@api_view(['POST'])
def reset_password(request):

    username = request.data.get("username")
    new_password = request.data.get("new_password")

    try:

        user = User.objects.get(username=username)

        user.set_password(new_password)
        user.save()

        return Response({
            "message": "Password updated successfully"
        })

    except User.DoesNotExist:

        return Response({
            "error": "User not found"
        }, status=404)
    

# -----------------------------------
# MEN PRODUCTS
# HOMEPAGE PRODUCTS show all men products
# -----------------------------------

class MenProductsView(
    generics.ListAPIView
):

    serializer_class = ProductCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name='Men'
        ).prefetch_related('images')
    


# -----------------------------------
# MEN HOMEPAGE PRODUCTS
# ONLY SELECTED PRODUCTS
# -----------------------------------

class MenHomepageProductsView(
    generics.ListAPIView
):

    serializer_class = ProductCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name='Men',
            show_in_homepage=True
        ).prefetch_related('images')
    


# -----------------------------------
# WOMEN HOMEPAGE PRODUCTS
# ONLY SELECTED PRODUCTS
# -----------------------------------

class WomenHomepageProductsView(
    generics.ListAPIView
):

    serializer_class = ProductCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name='Women',
            show_in_homepage=True
        ).prefetch_related('images')
    

class KidsHomepageProductsView(
    generics.ListAPIView
):

    serializer_class = ProductCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name='Kids',
            show_in_homepage=True
        ).prefetch_related('images')
    


# ----------MenTravel Bag----------
class MenTravelBagProductsView(
    generics.ListAPIView
):

    serializer_class = ProductCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Men",
            product_type__name="Bag",
            subcategory__name="travelbag"
        ).prefetch_related(
            "images"
        )
    

# ----------Mendufflebag-----

class MenDuffleBagProductsView(
    generics.ListAPIView
):

    serializer_class = DuffleCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Men",
            product_type__name="Bag",
            subcategory__name="dufflebag"
        ).prefetch_related(
            "images"
        )
    
# ------------menbrief------------------

class MenBriefBagProductsView(
    generics.ListAPIView
):

    serializer_class = BriefCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Men",
            product_type__name="Bag",
            subcategory__name="briefcase"
        ).prefetch_related(
            "images"
        )

# ------------mencross--------------

class MenCrossBagProductsView(
    generics.ListAPIView
):

    serializer_class = CrossCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Men",
            product_type__name="Bag",
            subcategory__name="crossbodybag"
        ).prefetch_related(
            "images"
        )
    
# -----------MenWallet---------
class MenWalletBagProductsView(
    generics.ListAPIView
):

    serializer_class = MenWalletCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Men",
            product_type__name="Wallet",
          
        ).prefetch_related(
            "images"
        )

# -----------menbelt-----------

class MenBeltBagProductsView(
    generics.ListAPIView
):

    serializer_class = MenBeltCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Men",
            product_type__name="Belt",
          
        ).prefetch_related(
            "images"
        )
    # -------------menshoe----------------

class MenShoesView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="Men",
            product_type__name="Footwear",
            subcategory__name="Shoe"
        )

        serializer = MenShoeCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)


# --------------menchelboot-----------

class MenChelseaView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="Men",
            product_type__name="Footwear",
            subcategory__name="Chelsea boot"
        )

        serializer = MenChelseaCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)

# ----------men des----------------

class MenDesertView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="Men",
            product_type__name="Footwear",
            subcategory__name="Desert boot"
        )

        serializer = MenDesertCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)
    

# ----------women handbag---------

class WomenHandView(generics.ListAPIView):

    serializer_class = WomenHandBagCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Women",
            product_type__name="Bag",
            subcategory__name="handbag"
        ).prefetch_related(
            "images"
        )
    
# -----------totebag-----------

class WomenToteView(generics.ListAPIView):

    serializer_class = WomenToteBagCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Women",
            product_type__name="Bag",
            subcategory__name="totebag"
        ).prefetch_related(
            "images"
        )


# ----slingbag-------------
class WomenSlingView(generics.ListAPIView):

    serializer_class = WomenSlingBagCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Women",
            product_type__name="Bag",
            subcategory__name="slingbag"
        ).prefetch_related(
            "images"
        )
    
# ------------women tr-------
class WomenTrView(generics.ListAPIView):

    serializer_class = WomenTrBagCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Women",
            product_type__name="Bag",
            subcategory__name="travelbag"
        ).prefetch_related(
            "images"
        )


# -----------women wallet-------------
class WomenWalletView(generics.ListAPIView):

    serializer_class = WomenWalletCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Women",
            product_type__name="Wallet",
            
        ).prefetch_related(
            "images"
        )

# --women belt---------
class WomenBeltView(generics.ListAPIView):

    serializer_class =WomenBeltCardSerializer

    def get_queryset(self):

        return Product.objects.filter(
            gender__name="Women",
            product_type__name="Belt",
            
        ).prefetch_related(
            "images"
        )

# ------------flip---------------------

class WomenFlipView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="Women",
            product_type__name="Footwear",
            subcategory__name="flipflops"
        )

        serializer = WomenFlipCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)


# ------------sandals--------------
class WomenSandalView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="Women",
            product_type__name="Footwear",
            subcategory__name="Sandals"
        )

        serializer = WomenSandalCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)
    
# ---loafer-------

class WomenLoaferView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="Women",
            product_type__name="Footwear",
            subcategory__name="Loafers"
        )

        serializer = WomenLoaferCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)
    
# -----------kids tr ----------------

class KidsTravelView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="kids",
            product_type__name="Bag",
            subcategory__name="travelbag"
        )

        serializer = KidsTravelCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)

# -------------backapck-----------------

class KidsBackpackView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="kids",
            product_type__name="Bag",
            subcategory__name="backpack"
        )

        serializer =  KidsBackPackCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)

# ---------------diaper bag-----------------
class KidsDiaperView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="kids",
            product_type__name="Bag",
            subcategory__name="diaperbag"
        )

        serializer =  KidsDiaperBagCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)
    
# -----------bagcharm-----------
class BagCharmView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="kids",
            product_type__name="Bag Charm",
            
        )

        serializer =  KidsBagcharmCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)
    
# -----------kidshoe-----------
class KidShoeView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="kids",
            product_type__name="Footwear",
            subcategory__name="Shoe"
        )

        serializer = KidShoeCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)

# ---------kid chel---------
class KidsChelView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="kids",
            product_type__name="Footwear",
            subcategory__name="chelsea boot"
        )

        serializer = KidChelCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)

# ---------kid del--------

class KidsDesView(APIView):

    def get(self, request):

        products = Product.objects.filter(
            gender__name="kids",
            product_type__name="Footwear",
            subcategory__name="desert boot"
        )

        serializer = KidDesCardSerializer(
            products,
            many=True,
            context={
                "request": request
            }
        )

        return Response(serializer.data)


# GET wishlist products

class WishlistListView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self,request):

        wishlist = Wishlist.objects.filter(
            user=request.user
        )


        serializer = WishlistSerializer(
            wishlist,
            many=True,
            context={
                "request":request
            }
        )


        return Response(serializer.data)






# ADD wishlist

class AddWishlistView(APIView):

    permission_classes = [IsAuthenticated]



    def post(self,request):


        product_id = request.data.get(
            "product_id"
        )


        product = Product.objects.get(
            id=product_id
        )


        wishlist,created = Wishlist.objects.get_or_create(

            user=request.user,

            product=product

        )


        return Response(
            {
                "message":"wishlist added"
            }
        )
    

# REMOVE wishlist


class RemoveWishlistView(APIView):

    permission_classes = [IsAuthenticated]



    def delete(self,request,product_id):


        Wishlist.objects.filter(

            user=request.user,

            product_id=product_id

        ).delete()



        return Response(

            {
                "message":"removed"
            }

        )
