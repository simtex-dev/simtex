from typing import IO, Any, Optional, TextIO

from src.misc.stdout import Signs
from src.utils.logger import Logger
from src.utils.config import Config


def headings(
        log: Logger,
        conf: Config,
        title: str,
        out_file: Optional[TextIO]
    ) -> None:
    """Create the headings of the LaTeX file."""

    SECTIONS: dict[str, str] = {
            "main": (
                    "\n"
                    r"% size config of sections"
                    "\n\sectionfont{\\fontsize{"
                    "<SECTION_SIZES>}{15}\selectfont}"
                ),
            "sub": (
                    "\subsectionfont{\\fontsize{"
                    "<SECTION_SIZES>}{15}\selectfont}"
                ),
            "subsub": (
                    "\subsubsectionfont{\\fontsize{"
                    "<SECTION_SIZES>}{15}\selectfont}"
                ),
        }

    headings: list[str] = [
            f"\documentclass[{conf.font_size}pt]{{{conf.doc_class}}}\n",
            f"% font\n\\usepackage{{{conf.doc_font}}}\n\n% packages"
        ]

    pkgs: str
    for pkgs in conf.packages:
        headings.append(f"\\usepackage{pkgs}")
    headings.append(
        f"\\usepackage[scaled={conf.cfont_scale}]{{{conf.code_font}}}"
    )

    sec_sizes: int
    sec_val: str
    for sec_sizes, sec_val in zip(
            conf.section_sizes.values(), SECTIONS.values()
        ):
        headings.append(
            sec_val.replace(
                "<SECTION_SIZES>", str(sec_sizes)
            )
        )

    lstconf: IO[Any]
    with open(conf.code_conf, "r", encoding="utf-8") as lstconf:
        headings.append(f"\n% lst listings config\n{lstconf.read()}")

    items: str
    for items in [
            f"\n% paper info\n\\title{{{title}}}",
            f"\\author{{{conf.author}}}",
            f"\date{{{conf.date}}}"
        ]:
        headings.append(items)

    try:
        print(f"{Signs.PROC} Writing headings to file ...")
        if out_file is not None:
            for items in headings:
                out_file.write(f"{items}\n")
        else:
            with open(
                    f"{conf.output_folder}/a.tex", "w", encoding="utf-8"
                ) as out_file:
                for items in headings:
                    out_file.write(f"{items}\n")


    except (
        IOError,
        SystemError,
        BlockingIOError,
        PermissionError
    ) as Err:
        log.logger("E", f"Encountered {Err}, aborting ...")
        raise SystemExit
