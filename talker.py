import re

from logzero import logger


class talk:
    def __init__(self) -> None:
        self.match_hallo = re.compile(
            r"([hH][aAäÄ][lL]{2}[oO]|[hH][iI]|[sS][eE][rR][vV][uU][sS]|[mM][oO][iI][nN]|[gG][rRüÜuUß][eE]{0,2}[sS]?)"
        )

    def parse(self, input_text: str) -> str:
        input_text = input_text.lower()
        if re.match(self.match_hallo, input_text):
            logger.debug("We have a match!")
            return "Hallo zurück"
        return "Das hab ich nicht verstanden, bitte nochmal"
