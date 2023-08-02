import os
import re
from datetime import datetime, timedelta
from typing import Generator

import requests
from bs4 import BeautifulSoup as Bs
from requests.exceptions import ConnectionError
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


def get_next_url(url: str, end: str) -> str:
    part = url.rsplit(end, maxsplit=1)[1][1:]
    if part.isnumeric():
        return re.sub(f'{part}$', str(int(part) + 1), url)

    return f'{url}-{Config.SUFFIX}'


def get_image_sources(content: bytes) -> list[str]:
    soup = Bs(content, 'html.parser')
    return [image['src'] for image in soup.find_all('img')]


def download_image(source: str, prefix: str):
    response = requests.get(Config.BASE_URL + source)
    filename = prefix + '-' + source.split('/')[-1]

    if not os.path.exists(Config.DOWNLOADS):
        os.mkdir(Config.DOWNLOADS)

    save_path = os.path.join(Config.DOWNLOADS, filename)
    with open(save_path, 'wb') as file:
        file.write(response.content)


def display_info(url: str, ok: bool, images_count: int):
    print(Colors.get_color(ok) + str(images_count), url + Colors.RESET)


def main():
    title = get_title()

    for date in date_generator():
        date_structure = Config.DATE_STRUCTURE.format(
            month=date.strftime('%m'),
            day=date.strftime('%d')
        )

        url = Config.URL.format(
            title=title,
            date=date_structure
        )

        while True:
            response = requests.get(url)
            image_sources = get_image_sources(response.content)
            prefix = url.rsplit('/', maxsplit=1)[1]
            display_info(url, response.ok, len(image_sources))

            if response.ok:
                if len(image_sources) > 0:
                    for image_source in image_sources:
                        try:
                            download_image(image_source, prefix)
                        except ConnectionError:
                            pass
                url = get_next_url(url, date_structure)
            else:
                break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye!')
