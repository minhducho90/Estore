from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT) #on_delete=models.CASCADE
    name = models.CharField(max_length=150, unique=True)
    image = models.ImageField(upload_to='store/images', default='store/images/default.png')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=250)
    price = models.FloatField(default=0.0) #models.IntegerField()
    price_origin = models.FloatField(null=True)
    image = models.ImageField(upload_to='store/images', default='store/images/default.png')
    content = models.TextField(null=True, blank=True)
    public_day = models.DateTimeField(auto_now_add=True)
    viewed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-public_day',)


class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=20, null=True)
    message = models.TextField()

    def __str__(self):
        return self.name