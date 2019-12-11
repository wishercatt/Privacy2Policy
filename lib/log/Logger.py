import logging
from logging import handlers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, level='info',
                 fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger()
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = logging.FileHandler(filename='output/log/log.log', mode='w', encoding='utf-8')
        th.setFormatter(format_str)

        self.logger.addHandler(sh)
        self.logger.addHandler(th)
        pass


LOGGER = Logger(level='info').logger

if __name__ == '__main__':
    log = Logger(level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('warn')
    log.logger.error('报错')
    log.logger.critical('严重')
