from elasticsearch_dsl import Document, Text, Keyword, Float
from elasticsearch_dsl.connections import connections
from .models import Product

connections.create_connection(
    hosts=['https://localhost:9200'],
    http_auth=('elastic' '7zMTFZJ5tV-D1Xuw9-XU'),
    )

class ProductIndex(Document):
    name = Text()
    description = Text()
    catalog_code = Keyword()
    price = Float()
    
    class Index:
        name = 'products'
        
    def save(self, **kwargs):
        return super().save(**kwargs)
    
def index_products():
    for product in Product.objects.all():
        product_doc = ProductIndex(
            meta={'id': product.id},
            name=product.name,
            description=product.description,
            catalog_code=product.catalog_code,
            price=product.price
        )
        product_doc.save()
    