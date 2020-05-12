import os
import configparser

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')
cfg = configparser.ConfigParser()
cfg.read(cfg_path)

if cfg.remove_option('bing', 'test'):
    cfg.write(open(cfg_path, 'w'))
    print('OK')
else:
    print('Bad')
