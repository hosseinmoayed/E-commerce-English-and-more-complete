from django.contrib import admin

# Register your models here.
from dashboard_module.models import Cart, Item, Discountcodes, UserDiscountCode, UserInfo, Comment

admin.site.register(Cart)
admin.site.register(Item)
admin.site.register(Discountcodes)
admin.site.register(UserDiscountCode)
admin.site.register(UserInfo)
admin.site.register(Comment)
