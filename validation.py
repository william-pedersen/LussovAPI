from typing import Optional, Union

import re


class Validation:

    @staticmethod
    def email(_str: Union[str, bytes]) -> bool:
        return re.match(
            """(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""",
            _str
        ) != None

    @staticmethod
    def password(_str: Union[str, bytes], min: Optional[int] = 8, max: Optional[int] = 80) -> bool:
        return re.match(
            f'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{{{min},{max}}}$',
            _str
        ) != None

    @staticmethod
    def name(_str: Union[str, bytes], min: Optional[int] = 1, max: Optional[int] = 80) -> bool:
        return re.match(
            f'^(?=.*?[A-Za-zÀ-ÖØ-öø-ÿ]).{{{min},{max}}}$',
            _str
        ) != None