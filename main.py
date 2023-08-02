from datetime import datetime, timedelta
from typing import Generator, Union

import requests
from bs4 import BeautifulSoup as Bs
from transliterate import translit
from transliterate.exceptions import LanguageDetectionError

from config import Config, Colors


def get_title() -> str:
    title = input(Config.ENTER_TITLE)
    title = title.lower().replace(' ', '-')

    try:
        title = translit(title, reversed=True)
    except LanguageDetectionError:
        pass

    return title


def date_generator() -> Generator[datetime, None, None]:
    start_date = datetime(*Config.START_DATE)
    end_date = datetime(*Config.END_DATE)

    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def get_next_url(url: str) -> str:
    pass


def get_image_urls(content: bytes) -> list[str]:
    pass


def display_info(url: str, ok: bool, images_count: int):
    pass


def main():
    title = get_title()

    for date in date_generator():
        url = Config.URL.format(
            title=title,
            month=date.strftime('%m'),
            day=date.strftime('%d')
        )

        # response = requests.get(url)
        # if response.ok:
        #     image_urls = get_image_urls(response.content)

        print(url)


if __name__ == '__main__':
    main()
