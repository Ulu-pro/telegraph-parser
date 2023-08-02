class Config:
    URL = 'https://telegra.ph/{title}-{month}-{day}'
    ENTER_TITLE = 'Enter title: '

    START_DATE = (2000, 1, 1)
    END_DATE = (2000, 12, 31)


class Colors:
    OK = '\033[92m'
    FAIL = '\033[91m'
    RESET = '\033[0m'

    @classmethod
    def get_color(cls, status) -> str:
        return cls.OK if status else cls.FAIL
