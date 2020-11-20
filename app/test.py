import os
import configparser

# from .log import Log

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')
if not os.path.exists(cfg_path):  # 如果不存在配置文件，就自动创建一个并恢复默认配置
    os.mknod(cfg_path)

cfg = configparser.ConfigParser()
cfg.read(cfg_path)

print(cfg.options('downloader'))
