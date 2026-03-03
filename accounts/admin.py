from django.contrib import admin
from .models import UserMostPurchase
from django.db.models import Value, Sum
from django.db.models.functions import Coalesce

# Register your models here.
class UserMostPurchaseAdmin(admin.ModelAdmin):
    readonly_fields = ["getTotalPurchases"]
    exclude = ('password', "last_login", "groups", "is_superuser", "is_staff", "user_permissions", "date_joined")
    show_in_index = True
    
    def get_queryset(self, request):
        qs = super().get_queryset(
            request
        ).filter(
            is_staff = False, 
            is_active = True
        ).annotate(
            item_count = Coalesce(
                Sum('order__item__quantity'),
                Value(0),
            )
        ).order_by(
            '-item_count'
        )

        max_subquery = qs.values("item_count")[:1]
        print(max_subquery)
        return qs.filter(item_count = max_subquery)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

admin.site.register(UserMostPurchase, UserMostPurchaseAdmin)