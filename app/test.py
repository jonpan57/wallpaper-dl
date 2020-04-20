import os

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'test.ini')
# 如果不存在cfg.ini文件，就自动创建一个
if not os.path.exists(cfg_path):
    os.mknod(cfg_path)