import logging


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler('output.log')
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    logger.info('Logger is created.')