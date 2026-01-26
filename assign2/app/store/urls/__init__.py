from django.urls import include, path


urlpatterns = [
	path("", include("store.urls.book_urls")),
	path("", include("store.urls.order_urls")),
	path("", include("store.urls.customer_urls")),
	path("", include("store.urls.staff_urls")),
]

