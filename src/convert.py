from typing import TextIO

from src.utils.config import Config, Rules
from src.utils.config import Config
from src.utils.logger import Logger
from src.utils.tex.sections.headings import headings
from src.utils.tex.sections.body import body, format_body


def convert(
        log: Logger,
        rules: Rules,
        conf: Config,
        title: str,
        in_file: str,
    ) -> None:
    """Main program."""

    out_file: TextIO
    with open(
            f"{conf.output_folder}/{conf.filename}",
            "w",
            encoding="utf-8"
        ) as out_file:
        start: int = headings(log, conf, title, out_file)
        body(log, rules, in_file, out_file)

    format_body(log, start, out_file)
