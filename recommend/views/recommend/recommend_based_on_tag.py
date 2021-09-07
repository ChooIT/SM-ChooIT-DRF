import pandas as pd
import os
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


def get_recommendations(idx, cosine_sim, tag_df):
    # 모든 제품 대해서 해당 제품과의 유사도를 구합니다.
    sim_scores = list(enumerate(cosine_sim[idx]))
    # 유사도에 따라 제품들을 정렬합니다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 5개의 영화를 받아옵니다.
    sim_scores = sim_scores[1:5]

    # 가장 유사한 10개의 영화의 인덱스를 받아옵니다.
    movie_indices = [i[0] for i in sim_scores]

    # 가장 유사한 10개의 영화의 제목을 리턴합니다.
    return tag_df.iloc[movie_indices]


def get_recommendation_list_based_on_tag():
    tfidf = TfidfVectorizer()

    path = os.path.join(PATH, 'prod_tag.txt')
    tag_df = pd.read_csv(path)
    tag_df['raw_tag'] = tag_df['raw_tag'].fillna('')
    tfidf_matrix = tfidf.fit_transform(tag_df['raw_tag'])

    # 코사인 유사도
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return list(get_recommendations(1, cosine_sim, tag_df)['id'])
