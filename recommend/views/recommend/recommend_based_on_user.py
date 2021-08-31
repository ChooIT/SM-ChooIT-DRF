import json
from rpy2.robjects.packages import importr, PackageNotInstalledError
from rpy2.robjects import r


def get_recommendation_list_based_on_user(preference: dict) -> list:
    """
    user = {
      'prod_num': 1,
      'prod_num': 2,
      'prod_num': 3,
        ...
    }
    """
    importr('readxl')
    importr('writexl')
    importr('recommenderlab')
    importr('jsonlite')

    # training data 형식 만들기
    r('library(readxl)')
    r('product_rating_data <- read_excel('
      '"/Users/sngeunjng/Develops/ChewIT/recommend/views/recommend/product_rating_data.xlsx", '
      'sheet ="Sheet3")')
    r('product_rating_matrix <- as(as(product_rating_data, "matrix"), "realRatingMatrix")')
    product_rating_matrix = r('product_rating_matrix')

    # training 모델
    eval_scheme = r['evaluationScheme'](product_rating_matrix, method="split", train=0.9, given=10, goodRating=3)
    training_recommender = r['Recommender'](r['getData'](eval_scheme, "train"), "UBCF")

    preference = json.dumps(preference)
    user_data = r['fromJSON'](preference)
    user_data_frame = r['data.frame'](user_data)
    r['library']('writexl')
    r['write_xlsx'](user_data_frame, path="userdata.xlsx")
    r('user_rating_data <- read_excel("userdata.xlsx")')
    r('user_rating_matrix <- as(as(user_rating_data, "matrix"), "realRatingMatrix")')
    user_rating_matrix = r('user_rating_matrix')

    # predict
    recommendations = r['predict'](training_recommender, user_rating_matrix, n=10)
    recommendations_list = r['as'](recommendations, "list")

    return recommendations_list
