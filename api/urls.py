from django.urls import path, include

from .views import *

app_name = "api"

urlpatterns = [
    path('asset/', include(([
                                path('create/', CreatedAssetView.as_view(), name="created"),
                                path('list/', ListingAssetView.as_view(), name="listing"),
                            ], "asset"))
         ),
    path('transaction/', include(([
                                      path('create/', CreatedTransactionView.as_view(), name="created")
                                  ], "transaction")))
]
