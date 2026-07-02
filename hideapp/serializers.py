from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Wishlist
from .models import ProductVariant
from django.db import models

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

    class Meta:
        model = ProductImage
        fields = '__all__'


# -----------------------------------
# PRODUCT VARIANT
# -----------------------------------

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = '__all__'


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

    class Meta:
        model = Product

        fields = [
            'id',
            'name',
            'description',
            'gender',
            'product_type',
            'subcategory',
            'color',
            'material',
            'price',
            'stock',
            'has_variants',
            'created_at',
            'images',
            'variants',
        ]

# -----------------------------------
# REGISTER SERIALIZER
# -----------------------------------

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = CustomUser

        fields = [
            'id',
            'username',
            'email',
            'phone',
            'password'
        ]

    def create(self, validated_data):

        password = validated_data.pop('password')

        user = CustomUser(**validated_data)

        user.set_password(password)

        user.save()

        return user
# -----------------------------------
# LOGIN SERIALIZER
# -----------------------------------

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField()

    def validate(self, data):

        user = authenticate(

            username=data['username'],

            password=data['password']
        )

        if user and user.is_active:

            return {
                "username": user.username
            }

        raise serializers.ValidationError(
            "Invalid username or password"
        )
    
    
class LogoutSerializer(serializers.Serializer):

    message = serializers.CharField(
        default="Logout successful",
        read_only=True
    )    





# -----------------------------------
# PRODUCT CARD SERIALIZER
# HOMEPAGE / MEN PAGE
# -----------------------------------

class ProductCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):
        first = obj.images.first()

        if not first:
            return None

        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(first.image.url)

        return first.image.url
    

# ----------Men Travel Bag product-------

class ProductCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    

# ---------Men duffle bag--------

class DuffleCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    
# --------------men brief-----------------------

class BriefCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    
# ----------mencross------------------

class CrossCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    
# -----------MenWallet------------
class MenWalletCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    

# ---------menbelt-------------------

class MenBeltCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None


# -------------menshoe------------------

class MenShoeCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None


# ------------menboot--------------


class MenChelseaCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    
    # ---------------men desboot---------
class MenDesertCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None


# -----women handbag------------------

class WomenHandBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None


# ------------totebag-------------
class WomenToteBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    

# --------slingbag-----------

class WomenSlingBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    
# ------------women tr------------------
class WomenTrBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None



# ----------women wallet---------
class WomenWalletCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# ----------women belt-------------
class WomenBeltCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# ----------------flip------------------
class WomenFlipCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# -----------sandals----------
class WomenSandalCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None
    
# ------------loafer-----------
class WomenLoaferCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# ----------------kids trbag----------

class KidsTravelCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# -------------backpack----------

class KidsBackPackCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None


# ----------diaper bag----------


class KidsDiaperBagCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# ------------bagcharm-----------------
class KidsBagcharmCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# ----------kid shoe------------
class KidShoeCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# -----------------kid chel-------
class KidChelCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None

# -------kids des---------
class KidDesCardSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        first_image = obj.images.first()

        if first_image:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(
                    first_image.image.url
                )

            return first_image.image.url

        return None


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