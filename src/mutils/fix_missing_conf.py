from requests import get

from src.mutils.merge_conf import merge_conf
from src.utils.logger import Logger


def fix_missing_config(
        log: Logger,
        log_msg: str,
        CONF_PATH: str,
        conf: bool = False,
        code_conf: bool = False,
        devel: bool = False,
        missing: bool = True
    ) -> None:
    """Downloads the original config file from github if not found.

    Args:
        log -- for logging.
        log_msg -- message that will be logged.
        CONF_PATH -- path of the config file.
        conf, code_conf -- whether the missing config is the code config
            or the main, simtex.json.
        devel -- whether to pull from devel or stable branch.
    """

    # this was done instead of packaging the config from
    # package data, so that the user will be able to
    # interact with the config file easily.

    if devel:
        branch: str = "devel"
    else:
        branch = "main"

    if conf:
        link: str = (
                "https://raw.githubusercontent.com/iaacornus"
                f"/simtex/{branch}/examples/config/simtex.json"
            )
        filename: str = "simtex.json" if missing else "simtex.json.bak"
    elif code_conf:
        link = (
                "https://raw.githubusercontent.com/iaacornus"
                f"/simtex/{branch}/examples/config/code_conf.txt"
            )
        filename = "code_conf.txt"

    for _ in range(3):
        try:
            log.logger("e", log_msg)
            with get(link, stream=True) as d_file:
                with open(
                        f"{CONF_PATH}/{filename}", "wb"
                    ) as conf_file:
                    for chunk in d_file.iter_content(chunk_size=1024):
                        if chunk:
                            conf_file.write(chunk)
        except (ConnectionError, IOError, PermissionError) as Err:
            log.logger(
                "E", f"{Err}. Cannot download {filename}, aborting ..."
            )
        else:
            log.logger("I", "Sucessfully fetched the config file.")
            if not missing:
                log.logger("I", "Updating existing config file ...")
                merge_conf(log, CONF_PATH)
            return

    raise SystemExit
