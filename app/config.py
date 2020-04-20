import os
import configparser
from app.log import Log

log = Log('config')
dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')


class Config:
    def __init__(self):
        self.cfg_path = cfg_path
        if not os.path.exists(cfg_path):
            log.warning('配置文件不存在，创建默认配置文件')
            self.restore()

        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.cfg_path)

    def config(self, option, value=None):  # 获取配置，同时可以修改配置
        if value:
            self._write(self.category, option, value)
            return self._get(self.category, option)
        else:
            return self._get(self.category, option)

    def _get(self, section, option):
        try:
            value = self.cfg.get(section, option)
        except configparser.NoSectionError:
            pass
        except configparser.NoOptionError:
            pass
        else:
            return value

    def _write(self, section, option, value):
        # 检查配置组是否不存在，不存在则添加配置组
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
        self.cfg.set(section, option, value)
        self.cfg.write(open(self.cfg_path, 'w'))

    def _remove(self, section, option):
        # 检查配置组是否存在，存在则删除配置项，否则不操作
        if self.cfg.has_section(section):
            self.cfg.remove_option(section, option)
            self.cfg.write(open(self.cfg_path, 'w'))
        else:
            pass

    def restore(self):
        backup = ''
        with open(self.cfg_path, mode='w', encoding='utf-8') as f:
            f.write(backup)