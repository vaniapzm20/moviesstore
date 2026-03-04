
from django.contrib import admin
from django.contrib.auth.models import User
from cart.models import Order

# Create your models here.
class UserMostPurchase(User):
    class Meta:
       proxy = True
       verbose_name = 'User w/ Most Purchases'
       verbose_name_plural = 'Users w/ Most Purchases'
    
    def getOrders(self): 
        return Order.objects.filter(user = self)

    @admin.display(description="Total purchases")
    def getTotalPurchases(self):
        purchases = 0
        orders = self.getOrders()
        # print("Orders:", orders)
        for order in orders:
            items = order.getItems()
            # print("Order:", order, "Items:", item)
            for item in items:
                purchases += item.quantity
        # print("Number of purchases:", purchases)
        return purchases

    def __str__(self):
        return str(self.username) + ' - ' + str(self.getTotalPurchases()) + ' movies bought'
    
class UserMostComment(User):
    class Meta:
        proxy = True
        verbose_name = 'User w/ Most Comments'
        verbose_name_plural = 'Users w/ Most Comments'

    def getComments(self):
        return self.review_set.all()
    
    @admin.display(description="Total comments")
    def getTotalComments(self):
        comments = self.getComments()
        return len(comments)
    
    def __str__(self):
        return str(self.username) + ' - ' + str(self.getTotalComments()) + ' comments'
