import os
import googleapiclient.discovery
import csv
import tqdm  # Это пакет чтобы интерактивно показывать прогресс в терминале при выполнении
import pandaW

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

API_KEY = "AIzaSyB4i6N9Csv2Ac6DdKctmn8r7DHzNOSaTOY"
VIDEO_IDS = ["Ywpd8M6wfHc", "sskg_JguH28", "JDKqXmOX52Q", "k8FIVugHGSg"]
COMMENT_COUNT = 1000
MAX_RESULT = 100


def print_hi():
    print('Start Analytics Script')  # Press Ctrl+F8 to toggle the breakpoint.


# Функция для скачивания комментариев по id видео
def get_comments(video_id, nextPageToken=None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Используем Youtube API
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    # Формируем параметры запроса
    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=MAX_RESULT,
        pageToken=nextPageToken,
        videoId=video_id,
        order="relevance"
    )
    # Метод youtube - выполнение запроса
    response = request.execute()

   #  print(response, "get_comments()")

    return response


# Функция для скачивания даты выхода видео по id
def get_video_date_published(video_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=API_KEY)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    # print(response, "get_video_date_published()")

    return response.get("items")[0].get("snippet").get("publishedAt")


# Парсинг данных
def youtube_comment_parser():
    # Запись в файл
    with open('comments.csv', 'w', encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator='\r')

        # Заголовки столбцов
        names = ['textOriginal',
                 'authorDisplayName',
                 'likeCount',
                 'publishedAt',
                 'videoPublishedAt']
        writer.writerow(names)

        iteration_count = int(COMMENT_COUNT / MAX_RESULT)
        for video_id in tqdm.tqdm(VIDEO_IDS):
            # Скачиваем комментарии
            items = []
            nextPageToken = None
            for _ in range(iteration_count):
                response = get_comments(video_id, nextPageToken)
                nextPageToken = response.get("nextPageToken")
                items = items + response.get("items")

            # Дата публикации видео
            videoPublishedAt = get_video_date_published(video_id)

            # Сохраняем комментарии и дату публикации видео в файл csv
            for item in items:
                topLevelComment = item.get("snippet").get("topLevelComment").get('snippet')

                row = [topLevelComment.get('textOriginal'),
                       topLevelComment.get('authorDisplayName'),
                       topLevelComment.get('likeCount'),
                       topLevelComment.get('publishedAt'),
                       videoPublishedAt]

                writer.writerow(row)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
    youtube_comment_parser()
    pandaW.show_histograms()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
