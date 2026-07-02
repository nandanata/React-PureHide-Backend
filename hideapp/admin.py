from django.contrib import admin



from .models import (
    GenderCategory,
    ProductType,
    SubCategory,
    Color,
    Product,
    ProductVariant,
    ProductImage,
)

admin.site.register(GenderCategory)

admin.site.register(ProductType)

admin.site.register(SubCategory)

admin.site.register(Color)

admin.site.register(Product)

admin.site.register(ProductVariant)

admin.site.register(ProductImage)
