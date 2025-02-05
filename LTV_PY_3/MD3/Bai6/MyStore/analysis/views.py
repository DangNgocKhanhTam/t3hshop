from django.shortcuts import render
import  pandas as pd
import os
from django.conf import settings
import numpy as np
from analysis.utils import get_hist
from store.models import Product

def work_with_series (request):
    views1 = pd.Series([[90006, 101141, 97297, 117182, 99637]])
    views1 = pd.DataFrame({'views': views1})
    view1_html = views1.to_html()

    likes = pd.Series([402, 389, 403, 397, 404])
    index = ["c1", "c2", "c3", "c4", "c5"]
    likes_df = pd.DataFrame({'likes': likes}, index=index)
    likes1_html = likes_df.to_html()

    views2 = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'analysis/data_views.csv'))
    headviews2 = views2.head().to_html()
    tailviews2 = views2.tail().to_html()

    len_views2 = len(views2)

    double_likes = likes.map(lambda x: x ** 2)
    double_likes_df = pd.DataFrame({'double_likes': double_likes})
    double_likes_html = double_likes_df.to_html()

    stats = likes.describe()
    stats_df = pd.DataFrame(stats)
    stats_html = stats_df.to_html()


    return render(request, 'analysis/series.html', {
        'views1':view1_html, 
        'like1': likes1_html,
        'headviews2': headviews2, 
        'tailviews2': tailviews2, 
        'len_views2': len_views2, 
        'double_likes': double_likes_html,
        'stats_html': stats_html
    })

def work_with_dataframe(request):
    # Tạo dataframe
    views_likes = np.array([[90006, 402], [101141, 389], [97297, 403], [117182, 397]])
    df_views_likes = pd.DataFrame(views_likes, columns=["views", "likes"])
    df_views_likes_html = df_views_likes.to_html()

    dic_views_like = {"views": [90006, 101141, 97297, 117182], "likes": [402, 389, 403, 397]}
    df2_views_likes = pd.DataFrame(dic_views_like)

    # Lấy thông tin cơ bản của dataframe
    data_info = df_views_likes.info()

    # Lấy các dòng đầu của dataframe
    data_head = df_views_likes.head()

    return render(request, "analysis/dataframe.html", {
        'df_views_likes_html': df_views_likes_html,
        'data_info': data_info,
        'data_head': data_head
    })

def work_with_chart_1(request):
    data_second = Product.objects.all()
    hist = get_hist(data_second, 'name', 'price_origin')
    return render(request, 'analysis/chart.html', {'hist':hist})




