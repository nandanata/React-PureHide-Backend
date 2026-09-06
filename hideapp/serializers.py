from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Wishlist,Cart
from .models import ProductVariant
from django.db import models
from .models import PlaceOrder
from django.utils import timezone

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


# -----------------------------------
# GENDER CATEGORY
# -----------------------------------

class GenderCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = GenderCategory
        fields = '__all__'


# -----------------------------------
# PRODUCT TYPE
# -----------------------------------

class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = '__all__'


# -----------------------------------
# SUBCATEGORY
# -----------------------------------

class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = '__all__'


# -----------------------------------
# COLOR
# -----------------------------------

class ColorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Color
        fields = '__all__'


# -----------------------------------
# PRODUCT IMAGE
# -----------------------------------

class ProductImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ["id", "image"]

    def get_image(self, obj):

        if not obj.image:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                obj.image.url
            )

        return obj.image.url


# -----------------------------------
# PRODUCT VARIANT
# -----------------------------------

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant

        fields = [
            "id",
            "product",
            "size",
            "stock",
        ]

# -----------------------------------
# PRODUCT
# -----------------------------------
class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    gender_name = serializers.CharField(
        source="gender.name",
        read_only=True
    )

    product_type_name = serializers.CharField(
        source="product_type.name",
        read_only=True
    )

    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True,
        allow_null=True
    )

    color_name = serializers.CharField(
        source="color.name",
        read_only=True
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "description",

            "gender",
            "gender_name",

            "product_type",
            "product_type_name",

            "subcategory",
            "subcategory_name",

            "color",
            "color_name",

            "material",
            "price",
            "stock",
            "has_variants",
            "created_at",

            "images",
            "variants",
        ]



# =========================================================
# REGISTER / UPDATE SERIALIZER
# =========================================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:

        model = CustomUser

        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'password'
        ]

        extra_kwargs = {
            'first_name': {
                'required': False
            },

            'last_name': {
                'required': False
            },

            'email': {
                'required': True
            },

            'phone': {
                'required': True
            },

            'username': {
                'required': False
            }
        }


    # =========================================================
    # CREATE USER
    # =========================================================

    def create(self, validated_data):

        password = validated_data.pop(
            'password',
            None
        )


        # -----------------------------------------------------
        # GET VALUES
        # -----------------------------------------------------

        username = (
            validated_data.get(
                'username',
                ''
            ) or ''
        ).strip()


        first_name = (
            validated_data.get(
                'first_name',
                ''
            ) or ''
        ).strip()


        last_name = (
            validated_data.get(
                'last_name',
                ''
            ) or ''
        ).strip()


        # =====================================================
        # USERNAME IS FULL NAME
        # =====================================================

        if username and not first_name and not last_name:

            name_parts = username.split()


            if len(name_parts) >= 2:

                first_name = name_parts[0]

                last_name = " ".join(
                    name_parts[1:]
                )

            else:

                first_name = username

                last_name = ""


        # -----------------------------------------------------
        # SAVE FIRST NAME
        # -----------------------------------------------------

        validated_data['first_name'] = first_name


        # -----------------------------------------------------
        # SAVE LAST NAME
        # -----------------------------------------------------

        validated_data['last_name'] = last_name


        # -----------------------------------------------------
        # CREATE FULL USERNAME
        # -----------------------------------------------------

        full_name = (
            f"{first_name} {last_name}"
        ).strip()


        if full_name:

            validated_data['username'] = full_name

        elif username:

            validated_data['username'] = username


        # =====================================================
        # CREATE USER
        # =====================================================

        user = CustomUser(
            **validated_data
        )


        if password:

            user.set_password(password)


        user.save()


        return user


    # =========================================================
    # UPDATE USER
    # =========================================================

    def update(
        self,
        instance,
        validated_data
    ):

        # -----------------------------------------------------
        # FIRST NAME
        # -----------------------------------------------------

        if 'first_name' in validated_data:

            instance.first_name = (
                validated_data['first_name'] or ''
            ).strip()


        # -----------------------------------------------------
        # LAST NAME
        # -----------------------------------------------------

        if 'last_name' in validated_data:

            instance.last_name = (
                validated_data['last_name'] or ''
            ).strip()


        # -----------------------------------------------------
        # EMAIL
        # -----------------------------------------------------

        if 'email' in validated_data:

            instance.email = (
                validated_data['email'] or ''
            ).strip()


        # -----------------------------------------------------
        # PHONE
        # -----------------------------------------------------

        if 'phone' in validated_data:

            instance.phone = (
                validated_data['phone'] or ''
            ).strip()


        # -----------------------------------------------------
        # PASSWORD
        # -----------------------------------------------------

        if 'password' in validated_data:

            password = validated_data.pop(
                'password'
            )


            if password:

                instance.set_password(
                    password
                )


        # -----------------------------------------------------
        # UPDATE USERNAME FROM NAME
        # -----------------------------------------------------

        first_name = (
            instance.first_name or ''
        ).strip()


        last_name = (
            instance.last_name or ''
        ).strip()


        full_name = (
            f"{first_name} {last_name}"
        ).strip()


        if full_name:

            instance.username = full_name


        # -----------------------------------------------------
        # SAVE
        # -----------------------------------------------------

        instance.save()


        return instance


# =========================================================
# USER ACCOUNT SERIALIZER
# =========================================================
#
# IMPORTANT:
# This serializer is ONLY for the Account page.
#
# It allows Account.jsx to receive:
#
# deletion_requested_at
# deletion_scheduled_for
#
# These fields are NOT shown on Register.jsx.
#
# from rest_framework import serializers

from .models import CustomUser


# =========================================================
# USER ACCOUNT SERIALIZER
# =========================================================

class UserAccountSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomUser

        fields = [

            'id',

            'username',

            'first_name',

            'last_name',

            'email',

            'phone',

            'profile_image',

            'deletion_requested_at',

            'deletion_scheduled_for'

        ]

        read_only_fields = [

            'username',

            'deletion_requested_at',

            'deletion_scheduled_for'

        ]


    # =====================================================
    # UPDATE USER
    # =====================================================

    def update(self, instance, validated_data):


        # -------------------------------------------------
        # UPDATE FIRST NAME
        # -------------------------------------------------

        instance.first_name = validated_data.get(

            'first_name',

            instance.first_name

        )


        # -------------------------------------------------
        # UPDATE LAST NAME
        # -------------------------------------------------

        instance.last_name = validated_data.get(

            'last_name',

            instance.last_name

        )


        # -------------------------------------------------
        # UPDATE EMAIL
        # -------------------------------------------------

        instance.email = validated_data.get(

            'email',

            instance.email

        )


        # -------------------------------------------------
        # UPDATE PHONE
        # -------------------------------------------------

        instance.phone = validated_data.get(

            'phone',

            instance.phone

        )


        # -------------------------------------------------
        # UPDATE PROFILE IMAGE
        # -------------------------------------------------

        if 'profile_image' in validated_data:

            instance.profile_image = validated_data.get(
                'profile_image'
            )


        # -------------------------------------------------
        # CREATE USERNAME FROM FIRST + LAST NAME
        # -------------------------------------------------

        first_name = instance.first_name.strip()

        last_name = instance.last_name.strip()


        new_username = (

            f"{first_name} {last_name}"

        ).strip()


        # -------------------------------------------------
        # CHECK USERNAME
        # -------------------------------------------------

        if new_username:

            username_exists = CustomUser.objects.filter(

                username=new_username

            ).exclude(

                pk=instance.pk

            ).exists()


            if username_exists:

                raise serializers.ValidationError({

                    'username':

                    'This username is already being used by another user.'

                })


            # -------------------------------------------------
            # UPDATE USERNAME AUTOMATICALLY
            # -------------------------------------------------

            instance.username = new_username


        # -------------------------------------------------
        # SAVE USER
        # -------------------------------------------------

        instance.save()


        return instance

# =========================================================
# LOGIN SERIALIZER
# =========================================================

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        allow_blank=False
    )


    password = serializers.CharField(
        required=True,
        allow_blank=False,
        write_only=True
    )


    def validate(self, data):

        username = data.get(
            "username"
        )


        password = data.get(
            "password"
        )


        # =====================================================
        # AUTHENTICATE USER
        # =====================================================

        user = authenticate(
            username=username,
            password=password
        )


        if not user:

            raise serializers.ValidationError({

                "detail":
                    "Invalid username or password."

            })


        # =====================================================
        # ACTIVE ACCOUNT CHECK
        # =====================================================

        if not user.is_active:

            raise serializers.ValidationError({

                "detail":
                    "This account is inactive."

            })


        # =====================================================
        # ADMIN LOGIN
        # =====================================================

        if user.is_staff or user.is_superuser:

            return {
    "id": user.id,
    "username": user.username,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "email": user.email,
    "phone": getattr(user, "phone", ""),
    "role": "admin",
    "is_admin": True
}


        # =====================================================
        # CUSTOMER LOGIN
        # =====================================================
        #
        # IMPORTANT:
        #
        # Customers whose account is scheduled for deletion
        # CAN STILL LOGIN during the 7-day period.
        #
        # There is intentionally NO deletion check here.
        #
        # =====================================================

        return {
    "id": user.id,
    "username": user.username,
    "first_name": user.first_name,
    "last_name": user.last_name,
    "email": user.email,
    "phone": getattr(user, "phone", ""),
    "role": "user",
    "is_admin": False
}


# =========================================================
# LOGOUT SERIALIZER
# =========================================================

class LogoutSerializer(
    serializers.Serializer
):

    message = serializers.CharField(

        default="Logout successful",

        read_only=True

    )
    
# -----------------------------------
# FORGOT PASSWORD SERIALIZER
# -----------------------------------

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


# -----------------------------------
# VERIFY OTP SERIALIZER
# -----------------------------------

class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)


# -----------------------------------
# RESET PASSWORD SERIALIZER
# -----------------------------------

class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    new_password = serializers.CharField(
        min_length=8,
        write_only=True
    )


# -----------------------------------
# PRODUCT CARD SERIALIZER
# HOMEPAGE / MEN PAGE / KIDS PAGE
# -----------------------------------
class ProductCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    color = serializers.CharField(
        source="color.name",
        read_only=True
    )

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(
                first.image.url
            )

        return first.image.url
    

# -----------------------------------
# ADMIN PRODUCT SERIALIZER
# -----------------------------------

class AdminProductSerializer(serializers.ModelSerializer):

    # -----------------------------------
    # DISPLAY NAMES
    # -----------------------------------

    gender_name = serializers.CharField(
        source="gender.name",
        read_only=True
    )

    product_type_name = serializers.CharField(
        source="product_type.name",
        read_only=True
    )

    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True,
        allow_null=True
    )

    color_name = serializers.CharField(
        source="color.name",
        read_only=True,
        allow_null=True
    )

    # -----------------------------------
    # PRODUCT IMAGE
    # -----------------------------------

    image = serializers.SerializerMethodField()

    # -----------------------------------
    # STOCK STATUS
    # -----------------------------------

    status = serializers.SerializerMethodField()

    # -----------------------------------
    # PRODUCT VARIANTS
    #
    # Used by Admin Product View page.
    # If product has no variants,
    # this will return an empty list.
    # -----------------------------------

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    # -----------------------------------
    # META
    # -----------------------------------

    class Meta:

        model = Product

        fields = [

            # -----------------------------------
            # BASIC PRODUCT
            # -----------------------------------

            "id",
            "name",
            "description",

            # -----------------------------------
            # CATEGORY
            # -----------------------------------

            "gender_name",
            "product_type_name",
            "subcategory_name",

            # -----------------------------------
            # PRODUCT DETAILS
            # -----------------------------------

            "color_name",
            "material",

            # -----------------------------------
            # PRICE / STOCK
            # -----------------------------------

            "price",
            "stock",

            # -----------------------------------
            # VARIANT FLAG
            # -----------------------------------

            "has_variants",

            # -----------------------------------
            # IMAGE
            # -----------------------------------

            "image",

            # -----------------------------------
            # VARIANTS
            # -----------------------------------

            "variants",

            # -----------------------------------
            # STATUS
            # -----------------------------------

            "status",

            # -----------------------------------
            # CREATED DATE
            # -----------------------------------

            "created_at",
        ]

    # =================================================
    # PRODUCT IMAGE
    # =================================================

    def get_image(self, obj):

        # Get the newest uploaded image
        image_obj = (
            obj.images
            .order_by("-id")
            .first()
        )

        if not image_obj or not image_obj.image:
            return None

        request = self.context.get("request")

        if request:

            return request.build_absolute_uri(
                image_obj.image.url
            )

        return image_obj.image.url

    # =================================================
    # STOCK STATUS
    # =================================================

    def get_status(self, obj):

        if obj.stock == 0:

            return "Out of Stock"

        elif obj.stock <= 10:

            return "Low Stock"

        return "In Stock"


    
# ----------Men Travel Bag product-------

class TravelProductCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
           "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    

# ---------Men duffle bag--------

class DuffleCardSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    
# --------------men brief-----------------------

class BriefCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
           "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    
# ----------mencross------------------

class CrossCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    
# -----------MenWallet------------
class MenWalletCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    

# ---------menbelt-------------------

class MenBeltCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
           "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url


# -------------menshoe------------------

class MenShoeCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url


# ------------menboot--------------


class MenChelseaCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    
    # ---------------men desboot---------
class MenDesertCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url


# -----women handbag------------------

class WomenHandBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url


# ------------totebag-------------
class WomenToteBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    

# --------slingbag-----------

class WomenSlingBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    
# ------------women tr------------------
class WomenTrBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
           "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url



# ----------women wallet---------
class WomenWalletCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# ----------women belt-------------
class WomenBeltCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# ----------------flip------------------
class WomenFlipCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# -----------sandals----------
class WomenSandalCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    
# ------------loafer-----------
class WomenLoaferCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# ----------------kids trbag----------

class KidsTravelCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# -------------backpack----------

class KidsBackPackCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url


# ----------diaper bag----------


class KidsDiaperBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# ------------bagcharm-----------------
class KidsBagcharmCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# ----------kid shoe------------
class KidShoeCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# -----------------kid chel-------
class KidChelCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

# -------kids des---------
class KidDesCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()
    color = serializers.CharField(source="color.name", read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
            "color",
            "material",
            "stock",
            "has_variants",
            "variants",
        ]

    def get_image(self, obj):
        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url


# -------------whishlist-----------
class WishlistSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField(
        source="product.id"
    )


    product_name = serializers.CharField(
        source="product.name"
    )


    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2
    )


    material = serializers.CharField(
        source="product.material"
    )


    gender = serializers.SerializerMethodField()


    color = serializers.SerializerMethodField()


    stock = serializers.SerializerMethodField()


    image = serializers.SerializerMethodField()


    variants = serializers.SerializerMethodField()



    class Meta:

        model = Wishlist

        fields = [

            "id",
            "product_id",
            "product_name",
            "price",
            "material",
            "gender",
            "color",
            "stock",
            "image",
            "variants"

        ]



    # DEBUG CHECK
    def to_representation(self, instance):

        print("PRODUCT:", instance.product.name)

        print("COLOR:", instance.product.color)

        print("STOCK:", instance.product.stock)

        print(
            "VARIANTS:",
            list(
                instance.product.variants.values()
            )
        )

        return super().to_representation(instance)



    def get_gender(self,obj):

        if obj.product.gender:

            return obj.product.gender.name

        return ""




    def get_color(self,obj):

        if obj.product.color:

            return obj.product.color.name

        return "N/A"




    def get_stock(self,obj):

        product = obj.product


        # products like shoes/boots/sandals
        if product.has_variants:


            total_stock = product.variants.aggregate(
                total=models.Sum("stock")
            )["total"]


            return total_stock or 0



        # normal products like bags/wallets
        return product.stock





    def get_image(self,obj):

        image = obj.product.images.first()


        if image:

            request = self.context.get("request")


            return request.build_absolute_uri(
                image.image.url
            )


        return None





    def get_variants(self,obj):

        product = obj.product


        if product.has_variants:


            return [

                {

                    "id": variant.id,

                    "size": variant.size,

                    "stock": variant.stock

                }

                for variant in product.variants.all()

            ]


        return []

# -------------cart----------------------(to show slidebar)

class CartSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField(
        source="product.id",
        read_only=True
    )

    name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    color = serializers.CharField(
        source="product.color.name",
        read_only=True
    )

    image = serializers.SerializerMethodField()


    class Meta:

        model = Cart

        fields = [
            "id",
            "product_id",
            "name",
            "price",
            "color",
            "image",
            "quantity",
        ]


    def get_image(self, obj):

        # IMPORTANT:
        # Images belong to Product, not Cart

        first = (
            obj.product.images
            .order_by("-id")
            .first()
        )


        if not first:
            return None


        request = self.context.get(
            "request"
        )


        if request:

            return request.build_absolute_uri(
                first.image.url
            )


        return first.image.url

# ----------------mould page-----------------
class MouldWomenSlingSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:

        model = Product

        fields = [

            "id",

            "name",

            "price",

            "image",

            "color",

            "material",

            "stock",

            "has_variants"

        ]

    def get_image(self, obj):

        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:

            return request.build_absolute_uri(
                first.image.url
            )

        return first.image.url



# --------convoy page-------------------

class ConvoyBriefcaseSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:

        model = Product

        fields = [

            "id",

            "name",

            "price",

            "image",

            "color",

            "material",

            "stock",

            "has_variants"

        ]

    def get_image(self, obj):

        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url



# -----------------transit ---------------------

class TransitCrossSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:

        model = Product

        fields = [

            "id",

            "name",

            "price",

            "image",

            "color",

            "material",

            "stock",

            "has_variants"

        ]

    def get_image(self, obj):

        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    
# --------------Best seller--------------



class ProductBestSellerSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


# --------------------placeorder------------------------
# -----------------------------------
# PLACE ORDER
# -----------------------------------

class PlaceOrderSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_image = serializers.SerializerMethodField()

    variant_size = serializers.SerializerMethodField()

    class Meta:

        model = PlaceOrder

        fields = "__all__"

        read_only_fields = (
            "user",
            "product_price",
            "total_amount",
            "payment_status",
            "order_status",
            "created_at",
            "updated_at",
            "paid_at",
        )

    def get_product_image(self, obj):

        first = obj.images.order_by("-id").first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url

    def get_variant_size(self, obj):

        if obj.variant:
            return obj.variant.size

        return None



# ---------------cont info--------------------
class PlaceOrderContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaceOrder

        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "landmark",
            "district",
            "place",
            "pincode",
            "save_address",
        ]


# -----------------order summary-----------------
class OrderSummarySerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(source="product.name")

    product_image = serializers.SerializerMethodField()

    variant_size = serializers.SerializerMethodField()

    class Meta:
        model = PlaceOrder
        fields = [
            "id",

            "product_name",
            "product_image",
            "variant_size",

            "quantity",
            "product_price",
            "total_amount",

            "full_name",
            "phone",

            "address",
            "landmark",
            "district",
            "place",
            "pincode",
        ]

    def get_variant_size(self, obj):
        if obj.variant:
            return obj.variant.size
        return None

    def get_product_image(self, obj):

        image = obj.product.images.first()

        if not image:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(image.image.url)

        return image.image.url

# =========================================================
# ADMIN PRODUCT EDIT SERIALIZER
# =========================================================
class AdminProductEditSerializer(serializers.ModelSerializer):

    # =====================================================
    # DISPLAY NAMES
    # =====================================================

    gender_name = serializers.CharField(
        source="gender.name",
        read_only=True
    )

    product_type_name = serializers.CharField(
        source="product_type.name",
        read_only=True
    )

    subcategory_name = serializers.CharField(
        source="subcategory.name",
        read_only=True,
        allow_null=True
    )

    color_name = serializers.CharField(
        source="color.name",
        read_only=True,
        allow_null=True
    )

    # =====================================================
    # VARIANT FLAG
    # =====================================================

    has_variants = serializers.SerializerMethodField()

    # =====================================================
    # MAIN IMAGE
    # =====================================================

    image = serializers.SerializerMethodField()

    # =====================================================
    # ALL IMAGES
    # =====================================================

    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    # =====================================================
    # VARIANTS
    # =====================================================

    variants = ProductVariantSerializer(
        many=True,
        read_only=True
    )

    # =====================================================
    # DROPDOWN OPTIONS
    # =====================================================

    gender_options = serializers.SerializerMethodField()

    product_type_options = serializers.SerializerMethodField()

    subcategory_options = serializers.SerializerMethodField()

    color_options = serializers.SerializerMethodField()

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = Product

        fields = [

            "id",

            # -------------------------
            # PRODUCT
            # -------------------------

            "name",
            "description",

            # -------------------------
            # CATEGORY IDs
            # -------------------------

            "gender",
            "gender_name",

            "product_type",
            "product_type_name",

            "subcategory",
            "subcategory_name",

            "color",
            "color_name",

            # -------------------------
            # PRODUCT DETAILS
            # -------------------------

            "material",
            "price",
            "stock",

            "has_variants",

            # -------------------------
            # IMAGE
            # -------------------------

            "image",
            "images",

            # -------------------------
            # VARIANTS
            # -------------------------

            "variants",

            # -------------------------
            # DROPDOWN OPTIONS
            # -------------------------

            "gender_options",
            "product_type_options",
            "subcategory_options",
            "color_options",
        ]

    # =====================================================
    # HAS VARIANTS
    # =====================================================

    def get_has_variants(self, obj):

        return obj.variants.exists()

    # =====================================================
    # MAIN IMAGE
    # =====================================================

    def get_image(self, obj):

        image_obj = obj.images.order_by("-id").first()

        if not image_obj:
            return None

        if not image_obj.image:
            return None

        request = self.context.get("request")

        if request:

            return request.build_absolute_uri(
                image_obj.image.url
            )

        return image_obj.image.url

    # =====================================================
    # GENDER OPTIONS
    # =====================================================

    def get_gender_options(self, obj):

        return list(
            GenderCategory.objects.values(
                "id",
                "name"
            ).order_by("name")
        )

    # =====================================================
    # PRODUCT TYPE OPTIONS
    # =====================================================

    def get_product_type_options(self, obj):

        return list(
            ProductType.objects.values(
                "id",
                "name"
            ).order_by("name")
        )

    # =====================================================
    # SUBCATEGORY OPTIONS
    # =====================================================

    def get_subcategory_options(self, obj):

        return list(
            SubCategory.objects.values(
                "id",
                "name",
                "product_type_id"
            ).order_by("name")
        )

    # =====================================================
    # COLOR OPTIONS
    # =====================================================

    def get_color_options(self, obj):

        return list(
            Color.objects.values(
                "id",
                "name"
            ).order_by("name")
        )





# =========================================================
# ADMIN PRODUCT CREATE SERIALIZER
# =========================================================

class AdminProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product

        fields = [
            "name",
            "description",
            "gender",
            "product_type",
            "subcategory",
            "color",
            "material",
            "price",
            "stock",
            "has_variants",
            "show_in_homepage",
            "show_in_mould_women_sling",
            "show_in_convoy_briefcase",
            "show_in_transit_crossbag",
            "is_best_seller",
        ]

        extra_kwargs = {
            "subcategory": {
                "required": False,
                "allow_null": True
            },

            "color": {
                "required": False,
                "allow_null": True
            },

            "stock": {
                "required": False
            },
        }