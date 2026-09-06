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
from django.shortcuts import get_object_or_404
from .models import Wishlist, Cart
import random
import json
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser
)
from .models import Product
from .serializers import  WishlistSerializer
from .serializers import ProductCardSerializer
from .serializers import TravelProductCardSerializer
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
from .serializers import CartSerializer
from .serializers import MouldWomenSlingSerializer
from .serializers import PlaceOrderSerializer
from .serializers import PlaceOrderContactSerializer
from .serializers import OrderSummarySerializer
from .serializers import ConvoyBriefcaseSerializer
from .serializers import TransitCrossSerializer
from .serializers import ProductBestSellerSerializer
from .serializers import AdminProductSerializer
from .serializers import AdminProductEditSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
)
from django.db.models import Sum
from rest_framework import generics
from .models import ProductImage
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from random import randint
from .models import (
    Product,
    ProductVariant,
    ProductImage,
)

from .serializers import (
    AdminProductCreateSerializer,
    AdminProductEditSerializer,
)

from .models import CustomUser, PasswordResetOTP
from .models import (
    GenderCategory,
    ProductType,
    SubCategory,
    Color,
    Product,
    ProductVariant,
    ProductImage,
    CustomUser,PlaceOrder
    
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
    LoginSerializer,
     UserAccountSerializer

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



class ProductVariantDetailView(
    generics.RetrieveUpdateDestroyAPIView
):

    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

    def perform_update(self, serializer):

        variant = serializer.save()

        product = variant.product

        if product.has_variants:

            total_stock = product.variants.aggregate(
                total=Sum("stock")
            )["total"] or 0

            product.stock = total_stock

            product.save(
                update_fields=["stock"]
            )

    def perform_destroy(self, instance):

        product = instance.product

        instance.delete()

        if product.has_variants:

            total_stock = product.variants.aggregate(
                total=Sum("stock")
            )["total"] or 0

            product.stock = total_stock

            product.save(
                update_fields=["stock"]
            )

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


# -----------------------------------
# USER DETAIL / UPDATE VIEW
# -----------------------------------

# =========================================================
# USER DETAIL / UPDATE VIEW
# =========================================================

class UserDetailView(
    generics.RetrieveUpdateAPIView
):

    queryset = CustomUser.objects.all()

    serializer_class = UserAccountSerializer


    parser_classes = [

        MultiPartParser,

        FormParser,

        JSONParser

    ]




# =========================================================
# DELETE PROFILE IMAGE
# =========================================================

class DeleteProfileImageView(APIView):


    def delete(self, request, user_id):


        try:

            user = CustomUser.objects.get(
                id=user_id
            )


        except CustomUser.DoesNotExist:

            return Response(

                {
                    "detail":
                    "Customer account not found."
                },

                status=status.HTTP_404_NOT_FOUND

            )


        # =================================================
        # DELETE IMAGE FILE
        # =================================================

        if user.profile_image:

            image_path = user.profile_image.path


            # Remove database field first
            user.profile_image.delete(
                save=False
            )


            # Save empty value in database
            user.profile_image = None

            user.save(
                update_fields=[
                    "profile_image"
                ]
            )


            return Response(

                {
                    "message":
                    "Profile image deleted successfully."
                },

                status=status.HTTP_200_OK

            )


        return Response(

            {
                "message":
                "No profile image found."
            },

            status=status.HTTP_200_OK

        )

# -----------------------------------
# REQUEST ACCOUNT DELETION
# -----------------------------------

class RequestAccountDeletionView(APIView):

    def post(self, request, user_id):

        try:

            user = CustomUser.objects.get(
                id=user_id
            )

        except CustomUser.DoesNotExist:

            return Response(

                {
                    "detail":
                        "Customer account not found."
                },

                status=status.HTTP_404_NOT_FOUND

            )


        # -----------------------------------------------------
        # ALREADY SCHEDULED
        # -----------------------------------------------------

        if user.deletion_scheduled_for:

            return Response(

                {
                    "message":
                        "Account deletion is already scheduled.",

                    "deletion_scheduled_for":
                        user.deletion_scheduled_for
                },

                status=status.HTTP_200_OK

            )


        # -----------------------------------------------------
        # CURRENT TIME
        # -----------------------------------------------------

        now = timezone.now()


        # -----------------------------------------------------
        # DELETE AFTER 7 DAYS
        # -----------------------------------------------------

        deletion_date = (
            now + timedelta(days=7)
        )


        # -----------------------------------------------------
        # SAVE DELETION REQUEST
        # -----------------------------------------------------

        user.deletion_requested_at = now

        user.deletion_scheduled_for = (
            deletion_date
        )


        user.save(

            update_fields=[

                "deletion_requested_at",

                "deletion_scheduled_for"

            ]

        )


        # -----------------------------------------------------
        # RESPONSE
        # -----------------------------------------------------

        return Response(

            {

                "message":
                    "Account deletion scheduled successfully.",

                "deletion_requested_at":
                    user.deletion_requested_at,

                "deletion_scheduled_for":
                    user.deletion_scheduled_for

            },

            status=status.HTTP_200_OK

        )



# LOGIN VIEW
# -----------------------

class LoginView(APIView):

    def post(
        self,
        request
    ):

        serializer = LoginSerializer(
            data=request.data
        )

        # =====================================================
        # VALIDATE LOGIN
        # =====================================================

        if serializer.is_valid():

            data = serializer.validated_data

            return Response(
                {
                    "message": "Login successful",

                    "id": data["id"],

                    "username": data["username"],

                    "first_name": data.get(
                        "first_name",
                        ""
                    ),

                    "last_name": data.get(
                        "last_name",
                        ""
                    ),

                    "email": data["email"],

                    "phone": data.get(
                        "phone",
                        ""
                    ),

                    "role": data["role"],

                    "is_admin": data["is_admin"]
                },

                status=status.HTTP_200_OK
            )

        # =====================================================
        # LOGIN FAILED
        # =====================================================

        print(
            "LOGIN VALIDATION ERROR:",
            serializer.errors
        )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# -----------------------------------
# REGISTER VIEW
# -----------------------------------

class RegisterView(APIView):

    def post(
        self,
        request
    ):

        serializer = RegisterSerializer(
            data=request.data
        )


        if serializer.is_valid():

            serializer.save()


            return Response(

                {

                    "message":
                        "User registered successfully"

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

    def post(
        self,
        request
    ):

        logout(request)


        return Response(

            {

                "message":
                    "Logout successful"

            },

            status=status.HTTP_200_OK

        )
    

# -----------------------------------
# RESET PASSWORD


@api_view(["POST"])
def reset_password(request):

    email = request.data.get("email")
    new_password = request.data.get("new_password")


    try:
        user = CustomUser.objects.get(email=email)

    except CustomUser.DoesNotExist:

        return Response(
            {"error": "Invalid email"},
            status=status.HTTP_404_NOT_FOUND
        )


    try:
        otp_obj = PasswordResetOTP.objects.get(
            user=user,
            is_verified=True
        )

    except PasswordResetOTP.DoesNotExist:

        return Response(
            {"error": "Please verify OTP first"},
            status=status.HTTP_400_BAD_REQUEST
        )


    if otp_obj.is_expired():

        return Response(
            {"error": "OTP expired"},
            status=status.HTTP_400_BAD_REQUEST
        )


    user.set_password(new_password)
    user.save()


    return Response(
        {
            "message": "Password reset successful"
        },
        status=status.HTTP_200_OK
    )

# FORGOT PASSWORD
# -----------------------------------

@api_view(["POST"])
def forgot_password(request):

    print("forgot_password API called")

    email = request.data.get("email")

    if not email:
        return Response(
            {"error": "Email is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = CustomUser.objects.get(email=email)

    except CustomUser.DoesNotExist:
        return Response(
            {"error": "No account found with this email"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Generate OTP
    otp = str(randint(100000, 999999))

    # Delete previous OTP
    PasswordResetOTP.objects.filter(user=user).delete()

    # Save OTP
    try:
        saved_otp = PasswordResetOTP.objects.create(
            user=user,
            otp=otp,
            expires_at=timezone.now() + timedelta(minutes=10)
        )

        print("===================================")
        print("OTP SAVED SUCCESSFULLY")
        print("ID:", saved_otp.id)
        print("User:", saved_otp.user.email)
        print("OTP:", saved_otp.otp)
        print("Total OTP Records:", PasswordResetOTP.objects.count())
        print("===================================")

    except Exception as e:
        print("DATABASE ERROR:", e)

    # Send Email
    send_mail(
        subject="PureHide Password Reset OTP",
        message=f"""
Hello {user.username},

Your OTP for password reset is:

{otp}

This OTP will expire in 10 minutes.

If you didn't request this, please ignore this email.

Team PureHide
""",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response(
        {
            "message": "OTP sent successfully"
        },
        status=status.HTTP_200_OK
    )

# -----------------------------------
# VERIFY OTP
# # -----------------------------------
# VERIFY OTP
# -----------------------------------

@api_view(["POST"])
def verify_otp(request):

    email = request.data.get("email")
    otp = request.data.get("otp")


    if not email or not otp:
        return Response(
            {
                "error": "Email and OTP are required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )


    try:

        user = CustomUser.objects.get(
            email=email
        )


    except CustomUser.DoesNotExist:

        return Response(
            {
                "error": "Invalid email"
            },
            status=status.HTTP_404_NOT_FOUND
        )


    try:

        otp_obj = PasswordResetOTP.objects.get(
            user=user,
            otp=otp
        )


    except PasswordResetOTP.DoesNotExist:

        return Response(
            {
                "error": "Invalid OTP"
            },
            status=status.HTTP_400_BAD_REQUEST
        )


    # Check OTP expiry
    if otp_obj.is_expired():

        return Response(
            {
                "error": "OTP has expired"
            },
            status=status.HTTP_400_BAD_REQUEST
        )


    # Mark OTP as verified
    otp_obj.is_verified = True
    otp_obj.save()


    return Response(
        {
            "message": "OTP verified successfully",
            "email": user.email
        },
        status=status.HTTP_200_OK
    )




# =========================================================
# SCHEDULE CUSTOMER ACCOUNT DELETION
# =========================================================

class ScheduleAccountDeletionView(APIView):

    def post(self, request, user_id):

        try:

            user = CustomUser.objects.get(
                id=user_id
            )

        except CustomUser.DoesNotExist:

            return Response(
                {
                    "message": "Customer account not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # -------------------------------------------------
        # ALREADY SCHEDULED
        # -------------------------------------------------

        if user.deletion_scheduled_for:

            return Response(
                {
                    "message": "Account deletion is already scheduled.",
                    "deletion_scheduled_for":
                        user.deletion_scheduled_for
                },
                status=status.HTTP_200_OK
            )

        # -------------------------------------------------
        # SCHEDULE DELETION AFTER 7 DAYS
        # -------------------------------------------------

        deletion_date = (
            timezone.now() + timedelta(days=7)
        )

        user.deletion_scheduled_for = deletion_date

        user.save(
            update_fields=[
                "deletion_scheduled_for"
            ]
        )

        # -------------------------------------------------
        # IMPORTANT:
        # DO NOT DELETE USER
        # DO NOT LOGOUT USER
        # -------------------------------------------------

        return Response(
            {
                "message":
                    "Your account has been scheduled for deletion after 7 days.",

                "deletion_scheduled_for":
                    deletion_date
            },
            status=status.HTTP_200_OK
        )


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

class MenHomepageProductsView(generics.ListAPIView):

    serializer_class = ProductCardSerializer

    def get_queryset(self):
        return (
            Product.objects.filter(
                gender__name="Men",
                show_in_homepage=True
            )
            .prefetch_related("images")
        )


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

    serializer_class = TravelProductCardSerializer

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
    


# -----------------------------------
# ADMIN - ALL PRODUCTS
# -----------------------------------

class AdminProductListView(generics.ListAPIView):

    serializer_class = AdminProductSerializer

    def get_queryset(self):

        return (
            Product.objects
            .select_related(
                "gender",
                "product_type",
                "subcategory",
                "color"
            )
            .prefetch_related(
                "images",
                "variants"
            )
            .order_by("-created_at")
        )


# ---------------Best Seller------------------
@api_view(["GET"])
def best_seller_products(request):

    products = list(
        Product.objects.filter(is_best_seller=True)
    )

    random.shuffle(products)

    products = products[:4]

    serializer = ProductBestSellerSerializer(products, many=True)
    return Response(serializer.data)



# GET wishlist products

class WishlistListView(APIView):

    def get(self, request):

        user_id = request.query_params.get("user_id")
        guest_id = request.query_params.get("guest_id")


        # CUSTOMER
        if user_id:

            wishlist = Wishlist.objects.filter(
                user_id=user_id
            )


        # GUEST
        elif guest_id:

            wishlist = Wishlist.objects.filter(
                guest_id=guest_id
            )


        # NOTHING PROVIDED
        else:

            return Response(
                {
                    "detail": "user_id or guest_id is required."
                },
                status=400
            )


        serializer = WishlistSerializer(
            wishlist,
            many=True,
            context={
                "request": request
            }
        )


        return Response(
            serializer.data
        )



class AddWishlistView(APIView):

    def post(self, request):

        print("REQUEST DATA:", request.data)


        guest_id = request.data.get(
            "guest_id"
        )

        user_id = request.data.get(
            "user_id"
        )

        product_id = request.data.get(
            "product_id"
        )


        print(
            "USER ID:",
            user_id
        )

        print(
            "GUEST ID:",
            guest_id
        )

        print(
            "PRODUCT:",
            product_id
        )


        # PRODUCT REQUIRED
        if not product_id:

            return Response(
                {
                    "detail": "product_id is required."
                },
                status=400
            )


        product = get_object_or_404(
            Product,
            id=product_id
        )


        # CUSTOMER
        if user_id:

            user = get_object_or_404(
                CustomUser,
                id=user_id
            )


            Wishlist.objects.get_or_create(
                user=user,
                product=product
            )


        # GUEST
        elif guest_id:

            Wishlist.objects.get_or_create(
                guest_id=guest_id,
                product=product
            )


        # NO OWNER
        else:

            return Response(
                {
                    "detail":
                    "user_id or guest_id is required."
                },
                status=400
            )


        return Response(
            {
                "message": "Wishlist added"
            }
        )
    
class RemoveWishlistView(APIView):

    def delete(self, request, product_id):

        guest_id = request.data.get("guest_id")
        user_id = request.data.get("user_id")

        if user_id:

            Wishlist.objects.filter(

                user_id=user_id,

                product_id=product_id

            ).delete()

        else:

            Wishlist.objects.filter(

                guest_id=guest_id,

                product_id=product_id

            ).delete()

        return Response({
            "message": "Wishlist removed"
        })
    


# ---------------- CART ----------------

# GET cart products
class CartListView(APIView):

    def get(self, request):

        user_id = request.query_params.get(
            "user_id"
        )

        guest_id = request.query_params.get(
            "guest_id"
        )


        # -------------------------------
        # CUSTOMER CART
        # -------------------------------

        if user_id:

            cart = Cart.objects.filter(
                user_id=user_id
            )


        # -------------------------------
        # GUEST CART
        # -------------------------------

        elif guest_id:

            cart = Cart.objects.filter(
                guest_id=guest_id
            )


        # -------------------------------
        # NO OWNER
        # -------------------------------

        else:

            return Response(
                {
                    "error":
                    "user_id or guest_id is required"
                },
                status=400
            )


        serializer = CartSerializer(
            cart,
            many=True,
            context={
                "request": request
            }
        )


        return Response(
            serializer.data
        )


# ADD TO CART
class AddCartView(APIView):

    def post(self, request):

        guest_id = request.data.get(
            "guest_id"
        )

        user_id = request.data.get(
            "user_id"
        )

        product_id = request.data.get(
            "product_id"
        )


        print("CART REQUEST:")
        print("USER ID:", user_id)
        print("GUEST ID:", guest_id)
        print("PRODUCT ID:", product_id)


        # -------------------------------
        # PRODUCT REQUIRED
        # -------------------------------

        if not product_id:

            return Response(
                {
                    "error":
                    "product_id is required"
                },
                status=400
            )


        product = get_object_or_404(
            Product,
            id=product_id
        )


        # -------------------------------
        # CUSTOMER
        # -------------------------------

        if user_id:

            user = get_object_or_404(
                CustomUser,
                id=user_id
            )


            cart_item, created = (
                Cart.objects.get_or_create(
                    user=user,
                    product=product
                )
            )


        # -------------------------------
        # GUEST
        # -------------------------------

        elif guest_id:

            cart_item, created = (
                Cart.objects.get_or_create(
                    guest_id=guest_id,
                    product=product
                )
            )


        # -------------------------------
        # NO OWNER
        # -------------------------------

        else:

            return Response(
                {
                    "error":
                    "user_id or guest_id is required"
                },
                status=400
            )


        # -------------------------------
        # INCREASE QUANTITY
        # -------------------------------

        if not created:

            cart_item.quantity += 1

            cart_item.save()


        return Response(
            {
                "message":
                "Product added to cart"
            }
        )



    
# REMOVE FROM CART
class RemoveCartView(APIView):

    def delete(self, request, cart_id):

        guest_id = request.data.get(
            "guest_id"
        )

        user_id = request.data.get(
            "user_id"
        )


        # -------------------------------
        # CUSTOMER
        # -------------------------------

        if user_id:

            qs = Cart.objects.filter(
                id=cart_id,
                user_id=user_id
            )


        # -------------------------------
        # GUEST
        # -------------------------------

        elif guest_id:

            qs = Cart.objects.filter(
                id=cart_id,
                guest_id=guest_id
            )


        # -------------------------------
        # NO OWNER
        # -------------------------------

        else:

            return Response(
                {
                    "error":
                    "user_id or guest_id is required"
                },
                status=400
            )


        qs.delete()


        return Response(
            {
                "message":
                "removed successfully"
            }
        )


    

class UpdateCartView(APIView):

    def put(self, request, cart_id):

        guest_id = request.data.get(
            "guest_id"
        )

        user_id = request.data.get(
            "user_id"
        )

        quantity = request.data.get(
            "quantity"
        )


        # -------------------------------
        # CUSTOMER
        # -------------------------------

        if user_id:

            cart_item = Cart.objects.filter(
                id=cart_id,
                user_id=user_id
            ).first()


        # -------------------------------
        # GUEST
        # -------------------------------

        elif guest_id:

            cart_item = Cart.objects.filter(
                id=cart_id,
                guest_id=guest_id
            ).first()


        # -------------------------------
        # NO OWNER
        # -------------------------------

        else:

            return Response(
                {
                    "error":
                    "user_id or guest_id is required"
                },
                status=400
            )


        # -------------------------------
        # NOT FOUND
        # -------------------------------

        if not cart_item:

            return Response(
                {
                    "error":
                    "Cart item not found"
                },
                status=404
            )


        # -------------------------------
        # QUANTITY VALIDATION
        # -------------------------------

        if quantity is None:

            return Response(
                {
                    "error":
                    "quantity is required"
                },
                status=400
            )


        if int(quantity) < 1:

            return Response(
                {
                    "error":
                    "quantity must be at least 1"
                },
                status=400
            )


        cart_item.quantity = int(
            quantity
        )

        cart_item.save()


        return Response(
            {
                "message":
                "updated"
            }
        )


# ----------mould page--------------

class MouldWomenSlingProductsView(APIView):

    def get(self, request):

        products = Product.objects.filter(

            gender__name="Women",

            product_type__name="Bag",

            subcategory__name="slingbag",

            show_in_mould_women_sling=True

        ).prefetch_related("images")

        serializer = MouldWomenSlingSerializer(

            products,

            many=True,

            context={"request": request}

        )

        return Response(serializer.data)
    

# -------------convoy page-----------------

class ConvoyBriefcaseProductsView(APIView):

    def get(self, request):

        products = Product.objects.filter(

            gender__name="Men",

            product_type__name="Bag",

            subcategory__name="briefcase",

            show_in_convoy_briefcase=True

        ).prefetch_related("images")

        serializer = ConvoyBriefcaseSerializer(

            products,

            many=True,

            context={"request": request}

        )

        return Response(serializer.data)

# --------------transit-----------------

class TransitCrossProductsView(APIView):

    def get(self, request):

        products = Product.objects.filter(

            gender__name="Men",

            product_type__name="Bag",

            subcategory__name="crossbodybag",

            show_in_transit_crossbag=True

        ).prefetch_related("images")

        serializer = TransitCrossSerializer(

            products,

            many=True,

            context={"request": request}

        )

        return Response(serializer.data)


    
# -----------place order--------------
from decimal import Decimal

class PlaceOrderView(APIView):

    def post(self, request):

        user_id = request.data.get("user_id")
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))
        variant_id = request.data.get("variant_id")

        # -------------------------
        # Login Required
        # -------------------------

        if not user_id:
            return Response(
                {
                    "message": "Login required"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = get_object_or_404(
            CustomUser,
            id=user_id
        )

        product = get_object_or_404(
            Product,
            id=product_id
        )

        variant = None

        if variant_id:
            variant = get_object_or_404(
                ProductVariant,
                id=variant_id,
                product=product
            )

        product_price = product.price

        total_amount = Decimal(product_price) * quantity

        # ----------------------------------------
        # Get previously saved address
        # ----------------------------------------

        last_saved_address = (
            PlaceOrder.objects.filter(
                user=user,
                save_address=True
            )
            .exclude(
                full_name=""
            )
            .order_by("-created_at")
            .first()
        )

        # ----------------------------------------
        # Check if active checkout exists
        # ----------------------------------------

        order = PlaceOrder.objects.filter(
            user=user,
            is_order_completed=False
        ).first()

        if order:

            order.product = product
            order.variant = variant
            order.quantity = quantity
            order.product_price = product_price
            order.total_amount = total_amount

            order.save()

        else:

            order = PlaceOrder.objects.create(

                user=user,

                product=product,

                variant=variant,

                quantity=quantity,

                product_price=product_price,

                total_amount=total_amount,

            )

            # ----------------------------------------
            # Auto-fill saved address
            # ----------------------------------------

            if last_saved_address:

                order.full_name = last_saved_address.full_name
                order.email = last_saved_address.email
                order.phone = last_saved_address.phone
                order.address = last_saved_address.address
                order.landmark = last_saved_address.landmark
                order.district = last_saved_address.district
                order.place = last_saved_address.place
                order.pincode = last_saved_address.pincode
                order.save_address = True

                order.save()

        serializer = PlaceOrderSerializer(
            order,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )




# ==========================================
# GET CURRENT PLACE ORDER
# ==========================================

class CurrentPlaceOrderView(APIView):

    def get(self, request):

        user_id = request.query_params.get("user_id")

        if not user_id:

            return Response(
                {"error": "user_id required"},
                status=400
            )

        order = PlaceOrder.objects.filter(
            user_id=user_id,
            is_order_completed=False
        ).first()

        if not order:

            return Response(
                {"error": "No active order found"},
                status=404
            )

        serializer = PlaceOrderContactSerializer(order)

        return Response({

            "order_id": order.id,

            "product_id": order.product.id,

            "product_name": order.product.name,

            "quantity": order.quantity,

            "variant": order.variant.size if order.variant else None,

            "product_price": order.product_price,

            "total_amount": order.total_amount,

            "contact_information": serializer.data

        })





# ==========================================
# SAVE CONTACT INFORMATION
# ==========================================

class SaveContactInformationView(APIView):

    def put(self, request, order_id):

        user_id = request.data.get("user_id")

        order = get_object_or_404(
            PlaceOrder,
            id=order_id,
            user_id=user_id,
            is_order_completed=False
        )

        serializer = PlaceOrderContactSerializer(
            order,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            order.contact_completed = True
            order.save()

            return Response({

                "message": "Contact information saved",

                "next_page": "payment"

            })

        return Response(
            serializer.errors,
            status=400
        )

# ------------order summary------------
class OrderSummaryView(APIView):

    def get(self, request):

        user_id = request.query_params.get("user_id")

        order = get_object_or_404(
            PlaceOrder,
            user_id=user_id,
            is_order_completed=False
        )

        serializer = OrderSummarySerializer(
            order,
            context={"request": request}
        )

        return Response(serializer.data)





# =========================================================
# ADMIN PRODUCT DETAIL
# =========================================================

class AdminProductDetailView(
    generics.RetrieveAPIView
):
    queryset = (
        Product.objects
        .select_related(
            "gender",
            "product_type",
            "subcategory",
            "color",
        )
        .prefetch_related(
            "variants",
            "images",
        )
    )

    serializer_class = AdminProductSerializer





class AdminProductImageUpdateView(APIView):

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def patch(self, request, pk):

        product = get_object_or_404(
            Product,
            pk=pk
        )

        image = request.FILES.get("image")

        if not image:
            return Response(
                {
                    "error": "No image provided."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # -----------------------------------------
        # Existing first/main image
        # -----------------------------------------

        image_obj = (
            product.images
            .order_by("id")
            .first()
        )

        if image_obj:

            image_obj.image = image
            image_obj.save()

        else:

            ProductImage.objects.create(
                product=product,
                image=image
            )

        # -----------------------------------------
        # Return updated product
        # -----------------------------------------

        serializer = AdminProductEditSerializer(
            product,
            context={
                "request": request
            }
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )




from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Product,
    ProductVariant,
    ProductImage,
)

from .serializers import (
    AdminProductEditSerializer,
    ProductVariantSerializer,
)


# =========================================================
# ADMIN PRODUCT EDIT
# =========================================================


class AdminProductEditView(APIView):

    # =====================================================
    # GET PRODUCT
    # =====================================================

    def get(self, request, pk):

        product = get_object_or_404(

            Product.objects
            .select_related(
                "gender",
                "product_type",
                "subcategory",
                "color",
            )
            .prefetch_related(
                "variants",
                "images",
            ),

            pk=pk
        )

        serializer = AdminProductEditSerializer(

            product,

            context={
                "request": request
            }

        )

        return Response(

            serializer.data,

            status=status.HTTP_200_OK
        )

    # =====================================================
    # UPDATE PRODUCT
    # =====================================================

    @transaction.atomic
    def patch(self, request, pk):

        product = get_object_or_404(
            Product,
            pk=pk
        )

        # =================================================
        # PRODUCT IMAGE
        # =================================================

        new_image = request.FILES.get("image")

        # =================================================
        # PRODUCT DATA
        # =================================================

        product_data = {

            "name": request.data.get(
                "name",
                product.name
            ),

            "description": request.data.get(
                "description",
                product.description
            ),

            "material": request.data.get(
                "material",
                product.material
            ),

            "price": request.data.get(
                "price",
                product.price
            ),

            "stock": request.data.get(
                "stock",
                product.stock
            ),
        }

        # =================================================
        # FOREIGN KEYS
        # =================================================

        if "gender" in request.data:

            product_data["gender"] = request.data.get(
                "gender"
            )

        if "product_type" in request.data:

            product_data["product_type"] = request.data.get(
                "product_type"
            )

        if "subcategory" in request.data:

            value = request.data.get(
                "subcategory"
            )

            product_data["subcategory"] = (
                value
                if value not in ["", "null", None]
                else None
            )

        if "color" in request.data:

            value = request.data.get(
                "color"
            )

            product_data["color"] = (
                value
                if value not in ["", "null", None]
                else None
            )

        # =================================================
        # UPDATE PRODUCT
        # =================================================

        serializer = AdminProductEditSerializer(

            product,

            data=product_data,

            partial=True,

            context={
                "request": request
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        product = serializer.save()

        # =================================================
        # IMAGE UPDATE
        # =================================================

        if new_image:

            ProductImage.objects.create(

                product=product,

                image=new_image
            )

        # =================================================
        # UPDATE VARIANTS
        #
        # Frontend sends:
        #
        # variants = [
        #     {
        #         "id": 187,
        #         "size": "4",
        #         "stock": 10
        #     }
        # ]
        # =================================================

        variants_data = request.data.get(
            "variants"
        )

        if variants_data:

            import json

            if isinstance(
                variants_data,
                str
            ):

                try:

                    variants_data = json.loads(
                        variants_data
                    )

                except json.JSONDecodeError:

                    return Response(

                        {
                            "variants":
                                "Invalid variants data."
                        },

                        status=status.HTTP_400_BAD_REQUEST
                    )

        if isinstance(
            variants_data,
            list
        ):

            for variant_data in variants_data:

                variant_id = variant_data.get(
                    "id"
                )

                if not variant_id:
                    continue

                variant = get_object_or_404(

                    ProductVariant,

                    id=variant_id,

                    product=product
                )

                variant_serializer = ProductVariantSerializer(

                    variant,

                    data={
                        "size": variant_data.get(
                            "size",
                            variant.size
                        ),

                        "stock": variant_data.get(
                            "stock",
                            variant.stock
                        ),
                    },

                    partial=True
                )

                variant_serializer.is_valid(
                    raise_exception=True
                )

                variant_serializer.save()

        # =================================================
        # IMPORTANT:
        # RECALCULATE PRODUCT STOCK FROM ALL VARIANTS
        #
        # Example:
        #
        # Size 5 = 30
        # Size 6 = 30
        #
        # Product stock = 60
        #
        # This happens automatically after variant update.
        # =================================================

        if product.has_variants:

            total_stock = product.variants.aggregate(
                total=Sum("stock")
            )["total"] or 0

            product.stock = total_stock

            product.save(
                update_fields=["stock"]
            )

        # =================================================
        # REFRESH EVERYTHING
        # =================================================

        product.refresh_from_db()

        product = (

            Product.objects

            .select_related(
                "gender",
                "product_type",
                "subcategory",
                "color",
            )

            .prefetch_related(
                "variants",
                "images",
            )

            .get(
                pk=product.pk
            )
        )

        # =================================================
        # RETURN FINAL DATABASE STATE
        # =================================================

        updated_serializer = AdminProductEditSerializer(

            product,

            context={
                "request": request
            }
        )

        return Response(

            updated_serializer.data,

            status=status.HTTP_200_OK
        )




# -----------------------------------
# ADMIN PRODUCT DELETE
# -----------------------------------

from rest_framework import generics


class AdminProductDeleteView(
    generics.DestroyAPIView
):
    queryset = Product.objects.all()



# =========================================================
# ADMIN PRODUCT ADD
# =========================================================

class AdminProductCreateView(APIView):

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    @transaction.atomic
    def post(self, request):

        # =================================================
        # PRODUCT DATA
        # =================================================

        product_data = {
            "name": request.data.get("name", ""),
            "description": request.data.get("description", ""),
            "gender": request.data.get("gender"),
            "product_type": request.data.get("product_type"),

            "subcategory": (
                request.data.get("subcategory")
                if request.data.get("subcategory")
                not in ["", "null", None]
                else None
            ),

            "color": (
                request.data.get("color")
                if request.data.get("color")
                not in ["", "null", None]
                else None
            ),

            "material": request.data.get(
                "material",
                "Leather"
            ),

            "price": request.data.get(
                "price",
                0
            ),

            "stock": request.data.get(
                "stock",
                0
            ),

            "has_variants": (
                str(
                    request.data.get(
                        "has_variants",
                        "false"
                    )
                ).lower()
                == "true"
            ),

            "show_in_homepage": (
                str(
                    request.data.get(
                        "show_in_homepage",
                        "false"
                    )
                ).lower()
                == "true"
            ),

            "show_in_mould_women_sling": (
                str(
                    request.data.get(
                        "show_in_mould_women_sling",
                        "false"
                    )
                ).lower()
                == "true"
            ),

            "show_in_convoy_briefcase": (
                str(
                    request.data.get(
                        "show_in_convoy_briefcase",
                        "false"
                    )
                ).lower()
                == "true"
            ),

            "show_in_transit_crossbag": (
                str(
                    request.data.get(
                        "show_in_transit_crossbag",
                        "false"
                    ).lower()
                )
                == "true"
            ),

            "is_best_seller": (
                str(
                    request.data.get(
                        "is_best_seller",
                        "false"
                    )
                ).lower()
                == "true"
            ),
        }

        # =================================================
        # VALIDATE PRODUCT
        # =================================================

        serializer = AdminProductCreateSerializer(
            data=product_data
        )

        serializer.is_valid(
            raise_exception=True
        )

        product = serializer.save()

        # =================================================
        # VARIANTS
        # =================================================

        variants_data = request.data.get(
            "variants"
        )

        if variants_data:

            if isinstance(
                variants_data,
                str
            ):
                try:
                    variants_data = json.loads(
                        variants_data
                    )

                except json.JSONDecodeError:

                    return Response(
                        {
                            "variants":
                                "Invalid variants JSON."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        if product.has_variants:

            if not isinstance(
                variants_data,
                list
            ):

                return Response(
                    {
                        "variants":
                            "Variants are required for this product."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_stock = 0

            for variant_data in variants_data:

                size = variant_data.get(
                    "size"
                )

                stock = variant_data.get(
                    "stock",
                    0
                )

                if not size:
                    return Response(
                        {
                            "variants":
                                "Every variant must have a size."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                stock = int(stock or 0)

                ProductVariant.objects.create(
                    product=product,
                    size=str(size),
                    stock=stock
                )

                total_stock += stock

            # ---------------------------------------------
            # PRODUCT STOCK = TOTAL VARIANT STOCK
            # ---------------------------------------------

            product.stock = total_stock

            product.save(
                update_fields=["stock"]
            )

        # =================================================
        # PRODUCT IMAGE
        # =================================================

        images = request.FILES.getlist(
            "images"
        )

        # Also support the single "image" field
        if not images:

            single_image = request.FILES.get(
                "image"
            )

            if single_image:
                images = [single_image]

        # =================================================
        # SAVE IMAGES
        # =================================================

        for image in images:

            ProductImage.objects.create(
                product=product,
                image=image
            )

        # =================================================
        # RETURN COMPLETE PRODUCT
        # =================================================

        product = (
            Product.objects
            .select_related(
                "gender",
                "product_type",
                "subcategory",
                "color",
            )
            .prefetch_related(
                "variants",
                "images",
            )
            .get(
                pk=product.pk
            )
        )

        response_serializer = AdminProductEditSerializer(
            product,
            context={
                "request": request
            }
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )