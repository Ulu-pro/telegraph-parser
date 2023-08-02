class Config:
    BASE_URL = 'https://telegra.ph'
    URL = BASE_URL + '/{title}-{date}'
    SUFFIX = 2

    DATE_STRUCTURE = '{month}-{day}'
    IMAGE_PATTERN = r"/file/[^\s'\"<>]*"

    ENTER_TITLE = 'Enter title: '

    START_DATE = (2000, 1, 1)
    END_DATE = (2000, 12, 31)

    DOWNLOADS = 'images/'


class Colors:
    OK = '\033[92m'
    FAIL = '\033[91m'
    RESET = '\033[0m'

    @classmethod
    def get_color(cls, status) -> str:
        return cls.OK if status else cls.FAIL
