from django.contrib import admin
from .models import Tour, TourVariation, TourImage, TourCategory, TourFeatured
from restaurants.models import RestaurantLocation
# Register your models here.
# admin.site.register(Tour)


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1
    # max_num =


class TourVariationInline(admin.TabularInline):
    model = TourVariation
    extra = 1


class TourAdmin(admin.ModelAdmin):
    list_display = ["__str__", "price"]

    inlines = [
        TourImageInline,
        TourVariationInline
    ]

    class Meta:
        model = Tour


admin.site.register(TourVariation)
admin.site.register(TourImage)
admin.site.register(TourCategory)
admin.site.register(TourFeatured)
# class ProductImagesInline(admin.TabularInline):
#     model = Tour


# class Product2ImagesInline(admin.TabularInline):
#     model = RestaurantLocation


# class ProductsAdmin(admin.ModelAdmin):
#     inlines = [
#         Product2ImagesInline
#     ]


admin.site.register(Tour, TourAdmin)
