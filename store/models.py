from django.db import models

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class Collection(models.Model):
    title = models.CharField(max_length=255)  
    featured_product = models.ForeignKey('Product' , on_delete=models.SET_NULL ,null=True ,related_name='+')

    #used to show title on admin site
    def __str__(self):
        return self.title

    #order the column with title 
    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection , on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
    #used to show title on admin site
    def __str__(self):
        return self.title

     #order the column with title 
    class Meta:
        ordering = ['title']

class Customer(models.Model):
    first_name = models.CharField(max_length=255) 
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateTimeField(null=True)   
    #choice filed
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES =[
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER,'Silver'),
        (MEMBERSHIP_GOLD,'Gold')
    ]
    membership = models.CharField(max_length=1 , choices= MEMBERSHIP_CHOICES ,default=MEMBERSHIP_BRONZE)

    #Custom table name (instead of appname_product)
    # class Meta:
    #     db_table = 'store_customers'  # ✅ Correct option name
    #     indexes = [
    #         models.Index(fields=['last_name'])
    #     ]
    


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add= True)

    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING ,'Pending'),
        (PAYMENT_STATUS_COMPLETE , 'Complete'),
        (PAYMENT_STATUS_FAILED , 'Failed')
    ]
    payment_status= models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES ,default=PAYMENT_STATUS_PENDING) 
    
    customer = models.ForeignKey(Customer , on_delete=models.PROTECT)   


#for one to one field example customer is parent
# class Address(models.Model):
#     street = models.CharField(max_length=255)  
#     city = models.CharField(max_length=255) 
#     customer = models.ForeignKey(Customer , on_delete=models.CASCADE,primary_key=True)

#for one to many 1 customer can have many addresses so no PK
class Address(models.Model):
    street = models.CharField(max_length=255)  
    city = models.CharField(max_length=255) 
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)
    
class OrderItem(models.Model):
    order= models.ForeignKey(Order , on_delete=models.PROTECT)
    product = models.ForeignKey(Product , on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=6 , decimal_places=2)
    quantity = models.PositiveSmallIntegerField()

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()    


 

     