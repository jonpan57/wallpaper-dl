import os
import configparser


class Config:
    config_path = 'app/cfg.ini'
    cfg = configparser.ConfigParser()
    cfg.read(config_path)

    def config(self, option, value=None):
        if value:
            self._write(self.category, option, value)
            return self._get(self.category, option)
        else:
            return self._get(self.category, option)

    def _get(self, section, option):
        # 检查配置项是否存在，存在则返回配置值，否则返回空值
        if self.cfg.has_option(section, option):
            return self.cfg.get(section, option)
        else:
            return None

    def _write(self, section, option, value):
        # 检查配置组是否不存在，不存在则添加配置组
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
        self.cfg.set(section, option, value)
        self.cfg.write(open(self.config_path, 'w'))

    def _remove(self, section, option):
        # 检查配置组是否存在，存在则删除配置项，否则不操作
        if self.cfg.has_section(section):
            self.cfg.remove_option(section, option)
            self.cfg.write(open(self.config_path, 'w'))
        else:
            pass
