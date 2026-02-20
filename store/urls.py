from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter , DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('products', views.ProductViewSet , basename='products')
router.register('collections',views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(
    router ,
    'products' ,
    lookup ='product' )  # This creates 'product_pk' in URL
products_router.register('reviews' , views.ReviewViewSet , basename='product-review' )

urlpatterns = router.urls + products_router.urls

#for function and class view
# urlpatterns = [
#     # path('products/', views.product_list ),
#     path('products/', views.ProductList.as_view() ),
#     path('products/<int:pk>/', views.ProductDetail.as_view() ),
#     path('collections/', views.CollectionList.as_view() ),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view() , name='collection-detail'),
# ] 