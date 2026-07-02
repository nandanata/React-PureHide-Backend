from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings

class CustomUser(AbstractUser):

    username_validator = RegexValidator(
        regex=r'^[A-Za-z0-9 @.+\-_]+$',
        message="Username can contain spaces and letters."
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)


# -----------------------------------
# GENDER CATEGORY
# -----------------------------------

class GenderCategory(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# -----------------------------------
# PRODUCT TYPE
# -----------------------------------

class ProductType(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -----------------------------------
# SUBCATEGORY
# -----------------------------------

class SubCategory(models.Model):

    name = models.CharField(max_length=100)

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name


# -----------------------------------
# COLOR MODEL
# -----------------------------------

class Color(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# -----------------------------------
# PRODUCT MODEL
# -----------------------------------

class Product(models.Model):

    MATERIAL_CHOICES = [
        ('Leather', 'Leather'),
        ('Synthetic', 'Synthetic'),
    ]

    name = models.CharField(max_length=255)

    description = models.TextField()

    gender = models.ForeignKey(
        GenderCategory,
        on_delete=models.CASCADE,
        related_name='products'
    )

    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name='products'
    )

    subcategory = models.ForeignKey(
    SubCategory,
    on_delete=models.CASCADE,
    related_name='products',
    null=True,
    blank=True
)
    color = models.ForeignKey(
        Color,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    material = models.CharField(
        max_length=100,
        choices=MATERIAL_CHOICES,
        default='Leather'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    has_variants = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    show_in_homepage = models.BooleanField(
    default=False)

    def __str__(self):
        return self.name


# -----------------------------------
# PRODUCT VARIANTS
# FOOTWEAR SIZE MODEL
# -----------------------------------

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )

    size = models.CharField(max_length=20)

    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Size {self.size}"


# -----------------------------------
# PRODUCT IMAGES
# -----------------------------------

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='products/'
    )

    def __str__(self):
        return self.product.name





# ---------------whishlist--------


class Wishlist(models.Model):

    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="wishlist_items"
)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"