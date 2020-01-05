import os
import configparser

cfg_path = 'cfg.ini'  # 配置文件路径

cfg = configparser.ConfigParser()  # 创建ConfigParser对象
cfg.read(cfg_path)  # 读取配置文件


def get(section, option):  # gettter方式获取配置值
    # 检查配置项是否存在，存在则返回配置值，否则返回空值
    if cfg.has_option(section, option):
        return cfg.get(section, option)
    else:
        return None


def write(section, option, value):  # settter方式设置配置值
    # 检查配置组是否不存在，不存在则添加配置组
    if not cfg.has_section(section):
        cfg.add_section(section)
    cfg.set(section, option, value)  # 设置配置值
    cfg.write(open(cfg_path, 'w'))  # 写入配置文件


def remove(section, option):  # 删除配置想项
    # 检查配置组是否存在，存在则删除配置项，否则不操作
    if cfg.has_section(section):
        cfg.remove_option(section, option)
        cfg.write(open(cfg_path, 'w'))  # 写入配置文件
    else:
        pass
