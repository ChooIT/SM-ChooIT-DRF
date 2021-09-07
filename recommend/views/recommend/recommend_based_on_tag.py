import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

from recommend.models import Product, ProductTag

PATH = ''


def make_rec():
    products = pd.DataFrame(columns=['id', 'category', 'raw_tag'])
    for product in Product.objects.all():
        raw_tag = ''
        for product_tag in ProductTag.objects.filter(prod_id=product.prod_no):
            raw_tag += product_tag.tag.tag_text + ' '
        series = {
            'id': product.prod_no,
            'category': product.prod_category,
            'raw_tag': raw_tag
        }
        products = products.append(series, ignore_index=True)
    products.to_csv(PATH, sep=',')
