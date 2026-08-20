from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=100)
    owner_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.product_name


class TransactionRecord(models.Model):
    TRANSACTION_TYPES = [
        ('sale', 'Sale'),
        ('expense', 'Expense'),
    ]
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    transaction_date = models.DateField()
    is_anomaly = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"


class Advisory(models.Model):
    text = models.TextField()
    generated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Advisory ({self.generated_at})"