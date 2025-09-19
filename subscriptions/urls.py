from django.urls import path


from .views import PackageView, SubscriptionsView

urlpatterns = [
    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    path('packages/', PackageView.as_view(), name='package'),
]