import pandas as pd
import numpy as np


# После того, как получили данные начинаем их обрабатывать.
# Поместим данные из ранее полученного файла в дата фрейм:
def show_histograms():
    df = pd.read_csv('comments.csv')

    # Сначала посмотрим на гистограмму количества лайков:
    df['likeCount'].hist(bins=50)
    df['logLikeCount'] = np.log1p(df['likeCount'])

    # Приведение даты к типу datetime
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], format="%Y-%m-%dT%H:%M:%SZ")
    df['videoPublishedAt'] = pd.to_datetime(df['videoPublishedAt'], format="%Y-%m-%dT%H:%M:%SZ")

    # Разница между датами публикацией комментария и видео
    df['publishedDifference'] = (df['publishedAt'] - df['videoPublishedAt']).apply(lambda x: x.total_seconds()).astype(
        int)

    return
