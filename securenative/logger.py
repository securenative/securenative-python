import logging

enable_sn_logging = False


def sn_logging(msg):
    if enable_sn_logging:
        logging.info(msg)
