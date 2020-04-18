import os
import logging

path = 'log/'

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
%threadName)s   :   当前线程名称
"""


def get_logger(name, level=logging.DEBUG, when='midnight', backup_count=0):
    """
    记录日志
    :param name: 日志名称
    :param level: 日志等级
    :param when: 间隔时间
        S: 秒
        M: 分钟
        H: 小时
        D: 天
        W: 星期（interval==0 代表星期一）
        midnight: 每天凌晨
    :param backup_count: 备份文件的个数，若超过该值，就会自动删除
    :return: logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # 日志输出格式
    formatter = logging.Formatter()
    # 输出到控制台
    sh = logging.StreamHandler()
    # 输出到文件
    fh = logging.FileHandler()
    # 设置日志输出格式
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 添加到logger对象
    logger.setHandler(sh)
    logger.setHandler(fh)

    return logger
