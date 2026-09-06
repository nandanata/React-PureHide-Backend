from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):

    username_validator = RegexValidator(
        regex=r'^[A-Za-z0-9 @.+*_-]+$',
        message="Username can contain letters, numbers, spaces, @, ., +, *, - and _."
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=15
    )

      # =====================================================
    # PROFILE IMAGE
    # =====================================================

    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # ACCOUNT DELETION
    # -----------------------------------------------------

    deletion_requested_at = models.DateTimeField(
        null=True,
        blank=True
    )

    deletion_scheduled_for = models.DateTimeField(
        null=True,
        blank=True
    )
# -----------------------------------
# PASSWORD RESET OTP
# -----------------------------------

class PasswordResetOTP(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_otps"
    )

    otp = models.CharField(max_length=6)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    is_verified = models.BooleanField(
        default=False
    )

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

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
    
    show_in_mould_women_sling = models.BooleanField(default=False)

    show_in_convoy_briefcase = models.BooleanField(default=False)

    show_in_transit_crossbag = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)

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

    guest_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["guest_id", "product"],
                name="unique_guest_product"
            ),
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product"
            ),
        ]

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.product.name}"
        return f"{self.guest_id} - {self.product.name}"
    
# -----------add to bag---------------------


class Cart(models.Model):

    guest_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["guest_id", "product"],
                name="unique_guest_cart"
            ),
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_cart"
            ),
        ]

    def __str__(self):

        if self.user:
            return f"{self.user.username} - {self.product.name}"

        return f"{self.guest_id} - {self.product.name}"


# -----------place order------------------
class PlaceOrder(models.Model):

    ORDER_STATUS = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    ]

    PAYMENT_METHODS = [
        ("Razorpay", "Razorpay"),
        ("COD", "Cash On Delivery"),
    ]

    # -------------------------
    # USER
    # -------------------------

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    # -------------------------
    # PRODUCT
    # -------------------------

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    quantity = models.PositiveIntegerField(default=1)

    # Price at purchase time
    product_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Price × Quantity
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # -------------------------
    # CONTACT INFORMATION
    # -------------------------

    full_name = models.CharField(
        max_length=200,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    landmark = models.CharField(
        max_length=200,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    place = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )
    save_address = models.BooleanField(default=False)

    # Contact page completed?
    contact_completed = models.BooleanField(default=False)

    # -------------------------
    # PAYMENT
    # -------------------------

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHODS,
        blank=True
    )

    payment_status = models.CharField(
        max_length=30,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    razorpay_order_id = models.CharField(
        max_length=200,
        blank=True
    )

    razorpay_payment_id = models.CharField(
        max_length=200,
        blank=True
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # -------------------------
    # ORDER STATUS
    # -------------------------

    order_status = models.CharField(
        max_length=30,
        choices=ORDER_STATUS,
        default="Pending"
    )
    is_order_completed = models.BooleanField(
    default=False
)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"