from django.db import models

''' id in django model is default (id = models.AutoFiled(primary_key=True) '''


class Product(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    image = models.URLField(blank=True, null=True)  # works like charfield but has url valdiator
    price = models.FloatField(max_length=10)
    vat_percentage = models.FloatField(max_length=10, default=23)
    number = models.IntegerField()

    @property
    def price_netto(self):
        return (self.price * 100) / (100 + self.vat_percentage)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    category = models.CharField(max_length=32)

    def __str__(self):
        return self.category


class Client(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    company = models.CharField(max_length=64, blank=True, null=True)
    regon = models.CharField(max_length=9, blank=True, null=True)
    nip = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    city = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house_num = models.IntegerField()
    local_num = models.IntegerField(blank=True, null=True)
    post_num = models.CharField(max_length=10)

    def __str__(self):
        return self.street


class User(models.Model):
    login = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64)
    admin = models.BooleanField(default=False)
    wallet = models.FloatField(blank=True, null=True)
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.login


class Opinion(models.Model):
    score = models.IntegerField()
    text = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Order(models.Model):
    # date added automatically when first time created
    submition_date = models.DateField(auto_now_add=True)
    payed_date = models.DateField()
    sent_date = models.DateField()
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE)


class Shipment(models.Model):
    company = models.CharField(max_length=64)
    price = models.IntegerField()


class OrderedProducts(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    number = models.IntegerField()
