from django.db import models

# Create your models here.


class Product(models.Model):
    category = models.CharField(max_length=50)
    product_name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.category + ' - ' + self.product_name

class assistant(models.Model):
    username = models.CharField(max_length=30, )
    firstname = models.CharField(max_length=30, )
    lastname = models.CharField(max_length=30, )
        
    def __str__(self):
        return self.username

class LoginTracker(models.Model):
    username = models.ForeignKey(assistant,on_delete=models.CASCADE)
    log_in = models.DateTimeField(null=True,blank=False)
    log_out = models.DateTimeField(null=True, blank=False)

    def __str__(self):
        return ("%s, %s" % (self.username.username,self.pk))


class Transaction(models.Model):
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE,blank=False, null=False)
    assistant_username = models.ForeignKey(assistant, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return("%s, %s , %s , %s, %s" % (self.assistant_username.username,self.item.category,self.item.product_name,self.item.price,self.date))

