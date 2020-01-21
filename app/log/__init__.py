import os
import logging

log_path = '/home/administrator/PycharmProjects/wallpager-download-tool/app/log/'


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

    sh = logging.StreamHandler()

    logger.setHandler(sh)

    return logger
