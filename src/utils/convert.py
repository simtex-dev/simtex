from typing import Any, TextIO, NoReturn

from src.config import Config, Replacements, Rules
from src.utils.tex.parser.headings import headings
from src.utils.tex.parser.body import body
from src.mutils.format_body import format_body
from src.mutils.fix_file_path import fix_file_path
from src.mutils.fix_title import fix_title
from src.mutils.finalize import finalize
from src.utils.logger import Logger


def convert(
        log: Logger,
        args: Any,
        rules: Rules,
        config: Config,
        replacement: Replacements,
    ) -> str | NoReturn:
    """This unifies all the modules.

    Args:
        log -- for logging.
        args -- overrides received from arguments.
        rules -- rules that needs to be followed in translation.
        config -- configuration of the document metadata, which includes,
            formatting, packages to use among others, refer to simtex.json.
        replacements -- math symbols that will be replaced with latex commands.

    Returns:
        The filepath of the output file.
    """

    log.logger("I", f"Converting {args.in_file} ...")

    title = fix_title(
            log,
            args.title,
            args.in_file,
            args.filenametitle,
            args.assumeyes
        ).replace(
            "_", r"\_"
        )
    OFILE_PATH: str = fix_file_path(
            log,
            args.in_file,
            config.output_folder,
            args.filename,
            args.assumeyes
        )

    try:
        out_file: TextIO
        with open(OFILE_PATH, "w", encoding="utf-8") as out_file:
            start: int = headings(log, config, title, out_file)
            files: list[str] = body(
                    log, rules, replacement, args.in_file, out_file
                )

        format_body(log, config, start, OFILE_PATH)
        finalize(log, files, config.output_folder, args.in_file)
    except (IOError, PermissionError) as Err:
        log.logger(
            "E", f"{Err}. Cannot convert the file to LaTeX, aborting ..."
        )
        raise SystemExit

    return OFILE_PATH
