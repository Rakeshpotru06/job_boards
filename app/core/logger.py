import logging

def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename="app.log",
        filemode="a",
    )
    return logging.getLogger("job_board_logger")

logger = setup_logger()
