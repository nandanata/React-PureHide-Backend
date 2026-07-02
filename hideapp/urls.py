from django.urls import path
from . import views
from .views import (
    ColorListCreateView,
    ColorDetailView,
    ProductListCreateView,
    ProductDetailView,
    ProductVariantListCreateView,
    ProductVariantDetailView,
    ProductImageListCreateView,
    ProductImageDetailView,
    MenProductsView,
    MenHomepageProductsView,
    WomenHomepageProductsView,
    KidsHomepageProductsView,
    MenTravelBagProductsView,
    MenDuffleBagProductsView,
    MenBriefBagProductsView,
    MenCrossBagProductsView,
    MenWalletBagProductsView,MenBeltBagProductsView,MenShoesView,MenChelseaView,
    MenDesertView,WomenHandView,WomenToteView,WomenSlingView,WomenTrView,WomenWalletView,WomenBeltView,WomenFlipView,WomenSandalView,
    WomenLoaferView,KidsTravelView,KidsBackpackView,KidsDiaperView,BagCharmView, KidShoeView, KidsChelView,KidsDesView,AddWishlistView,
    RemoveWishlistView,
    WishlistListView
  
)

urlpatterns = [

    # REGISTER
    path(
        'register/',
        views.RegisterView.as_view(),
        name='register'
    ),

    # LOGIN
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),


  # LOGOUT
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),

    path('reset-password/', views.reset_password),

    # VIEW USER BY ID
    path(
        'users/<int:pk>/',
        views.UserDetailView.as_view(),
        name='user-detail'
    ),


    path(
        'gender/',
        views.GenderCategoryListCreateView.as_view(),
        name='gender'
    ),

    path(
        'gender/<int:pk>/',
        views.GenderCategoryDetailView.as_view(),
        name='gender-detail'
    ),

    path(
        'product-types/',
        views.ProductTypeListCreateView.as_view(),
        name='product-types'
    ),

    path(
        'product-types/<int:pk>/',
        views.ProductTypeDetailView.as_view(),
        name='product-type-detail'
    ),

    path(
        'subcategories/',
        views.SubCategoryListCreateView.as_view(),
        name='subcategories'
    ),


    path(
        'subcategories/<int:pk>/',
        views.SubCategoryDetailView.as_view(),
        name='subcategory-detail'
    ),


      path(
        'colors/',
        ColorListCreateView.as_view(),
        name='color-list-create'
    ),

    path(
        'colors/<int:pk>/',
        ColorDetailView.as_view(),
        name='color-detail'
    ),
    

    path(
        'products/',
        ProductListCreateView.as_view(),
        name='product-list-create'
    ),

    path(
        'products/<int:pk>/',
        ProductDetailView.as_view(),
        name='product-detail'
    ),


    path(
        'variants/',
        ProductVariantListCreateView.as_view(),
        name='variant-list-create'
    ),

    # view one + update + delete
    path(
        'variants/<int:pk>/',
        ProductVariantDetailView.as_view(),
        name='variant-detail'
    ),

     # create + view all
    path(
        'product-images/',
        ProductImageListCreateView.as_view(),
        name='product-image-list-create'
    ),

    # view one + update + delete
    path(
        'product-images/<int:pk>/',
        ProductImageDetailView.as_view(),
        name='product-image-detail'
    ),


  
        # -----to display products in men home--
        path(
            'men-products/',
            MenProductsView.as_view(),
            name='men-products'
        ),

        # ---to show selected product in men home--
        path(
            'men-homepage-products/',
            MenHomepageProductsView.as_view(),
            name='men-homepage-products'
        ),


        # ---to show selected product in women home--
        path(
            'women-homepage-products/',
            WomenHomepageProductsView.as_view(),
            name='women-homepage-products'
        ),

        path(
    'kids-homepage-products/',
    KidsHomepageProductsView.as_view()
),


      
    path(
        "men-travel-bags/",
        MenTravelBagProductsView.as_view(),
        name="men-travel-bags"
    ),

    path(
        "men-duffle-bags/",
       MenDuffleBagProductsView.as_view(),
        name="men-travel-bags"
    ),



    path(
        "men-brief-bags/",
        MenBriefBagProductsView.as_view(),
        name="men-travel-bags"
    ),

    path(
        "men-cross-bags/" ,
        MenCrossBagProductsView.as_view(), 
        name="men-travel-bags"
    ),

    path(
        "men-wallets/",
        MenWalletBagProductsView.as_view(),
        name="men-wallets"
    ),

    path(
        "men-belt/",
        MenBeltBagProductsView.as_view(),
        name="men-belts"
    ),

    path(
        "men-shoes/",
        MenShoesView.as_view(),
        name="men-shoes"
    ),

    path(
        "men-chel/",
        MenChelseaView.as_view(),
        name="men-chelsea"
    ),
    
    path(
        "men-des/",
        MenDesertView.as_view(),
        name="men-desert"  
    ),

    path(
        "women-handbag/",
        WomenHandView.as_view(),
        name="women-handbag"
    ),

    path(
        "totebag/",
        WomenToteView.as_view(),
        name="totebag"
    ),
    path(
        "slingbag/",
        WomenSlingView.as_view(),
        name="slingbag"
    ),
    path(
        "women-tr/",
        WomenTrView.as_view(),
        name="travelbag"
    ),
    path(
        "women-wallet/",
        WomenWalletView.as_view(),
        name="women-wallet"
    ),
    path(
        "women-belt/",
        WomenBeltView.as_view(),
        name="women-belt"

    ),
    path(
        "flip/",
        WomenFlipView.as_view(),
        name="flip"
    ),
    path(
    "sandal/",
    WomenSandalView.as_view(),
    name="sandal"
),
path(
    "loafer/",
    WomenLoaferView.as_view(),
    name="loafer"

),
path(
    "kids-tr/",
    KidsTravelView.as_view(),
    name="kids-tr"
),
path(
    "backpack/",
    KidsBackpackView.as_view(),
    name="backpack"
),
path(
    "diaper/",
    KidsDiaperView.as_view(),
    name="diaper"
),
path(
    "bagcharm/",
   BagCharmView.as_view(),
    name="bagcharm"
),
path(
    "kids-shoe/",
     KidShoeView.as_view(),
     name="KidShoe"
),
path(
    "kids-chel/",
     KidsChelView.as_view(),
     name="Kids-chel"
),
path(
    "kids-des/",
    KidsDesView.as_view(),
    name="kids-des"
),

path(
        "wishlist/",
        WishlistListView.as_view()
    ),

    path(
        "wishlist/add/",
        AddWishlistView.as_view()
    ),

    path(
        "wishlist/remove/<int:product_id>/",
        RemoveWishlistView.as_view()
    ),

]