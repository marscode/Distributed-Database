from django.contrib import admin
from .models import assistant, Product, LoginTracker,Transaction
from import_export.admin import ExportMixin
# Register your models here.

class ProductAdmin(ExportMixin,admin.ModelAdmin):
    #display all the product column to the admin template
    list_display = ['category',
                    'product_name',
                    'quantity',
                    'price',]
    #editable price
    list_filter = ['price']

    #keyword to search in terms of category or a product name
    search_fields = ['category','product_name']

    #page limit
    list_per_page = 50
    


class assistantAdmin(ExportMixin,admin.ModelAdmin):
    
    #displaying all the information of the assistant
    list_display = ['username',
                    'firstname',
                    'lastname',]

    list_filter = ['firstname', 'lastname']
    #keyword search based on username
    search_fields = ['username']

    list_per_page = 5


class LogInTracker(ExportMixin,admin.ModelAdmin):

    list_display = ['username',
                    'log_in',
                    'log_out'
                    ]

    list_per_page = 20
    search_fields = ['username']

    #disabling the add button in admin so that they cant add whoever assistant they want to login
    def has_add_permission(self, request, obj=None):
        return False


    def has_delete_permission(self,request,obj=None):
        return False

class TransactionAdmin(ExportMixin,admin.ModelAdmin):
    
    list_display = [
                    'assistant_username',
                    'item',
                    'quantity',
                    'total',
                    'date'
                ]
    list_per_page = 20
    search_fields = ['assistant_username','item']

admin.site.register(Product, ProductAdmin)
admin.site.register(assistant, assistantAdmin)
admin.site.register(LoginTracker, LogInTracker)
admin.site.register(Transaction,TransactionAdmin)