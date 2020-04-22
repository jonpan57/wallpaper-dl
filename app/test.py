import os
import configparser

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')
cfg = configparser.ConfigParser()
cfg.read(cfg_path)

s = cfg.get('bing', 'rot')
print(s)
