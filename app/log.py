import os
import logging

dir_path = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(dir_path, 'logs')
if not os.path.exists(log_path):  # 如果不存在logs文件夹，就自动创建一个
    os.mkdir(log_path)


class Log:
    def __init__(self, name, level=logging.DEBUG, when='D', interval=14, backup_count=0):
        """
        记录日志
        :param name: 日志名称
        :param level: 日志等级
        :param when: 间隔时间
                    S: 秒
                    M: 分钟
                    H: 小时
                    D: 天
                    W0 - W6: 周一至周日
                    midnight: 每天凌晨
        :param backup_count: 备份文件的个数，若超过该值，就会自动删除
        """
        self.logger = logging.getLogger(name)
        self.filename = os.path.join(log_path, '{}.log'.format(name))
        self.logger.setLevel(level)
        self.level = level
        self.when = when
        self.interval = interval
        self.backup_count = backup_count
        self.formatter = logging.Formatter(
            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        """
        %(asctime)s     :   日志的时间
        %(name)         :   日志对象的名称
        %(filename)s    :   不包含路径的文件名
        %(pathname)s    :   包含路径的文件名
        %(funcName)s	:   日志记录所在的函数名
        %(levelname)s   :   日志的级别名称
        %(message)s     :   具体的日志信息
        %(lineno)d      :   日志记录所在的行号
        %(pathname)s    :   完整路径
        %(process)d     :   当前进程ID
        %(processName)s :   当前进程名称
        %(thread)d      :   当前线程ID
        %(threadName)s  :   当前线程名称
        """

    def _console(self, level, message):
        # 输出到文件
        fh = logging.handlers.TimedRotatingFileHandler(self.filename, when=self.when, interval=self.interval,
                                                       backupCount=self.backup_count, encoding='utf-8')
        fh.setLevel(self.level)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 输出到控制台
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(self.formatter)
        self.logger.addHandler(sh)

        # 根据输出级别输出信息
        if level == 'debug':
            self.logger.debug(message)
        elif level == 'info':
            self.logger.info(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        elif level == 'critical':
            self.logger.critical(message)

        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(fh)
        self.logger.removeHandler(sh)

        # 关闭打开的文件
        fh.close()

    def debug(self, message):
        self._console('debug', message)

    def info(self, message):
        self._console('info', message)

    def warning(self, message):
        self._console('warning', message)

    def error(self, message):
        self._console('error', message)

    def critical(self, message):
        self._console('critical', message)
