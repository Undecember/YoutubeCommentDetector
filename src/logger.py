import logging

def GenLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    print('Inititialize logger', flush = True)
    file_handler = logging.FileHandler('logs/latest.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

logger = GenLogger()
