import os
import configparser
from app.log import Log

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')


class Config:
    def __init__(self, section):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.cfg_path)

        self.section = section
        self.log = Log('config')
        if not os.path.exists(cfg_path):
            self.log.warning('配置文件不存在，自动恢复默认配置')
            self.restore()

    def config(self, option, value=None):  # 获取配置，同时可以修改配置
        if value:
            self._write(self.section, option, value)
        return self._get(self.section, option)

    def _get(self, section, option):
        try:
            value = self.cfg.get(section, option)
        except configparser.NoSectionError:
            self.log.error('配置文件,查无此[{}]'.format(section))
            value = None
        except configparser.NoOptionError:
            self.log.error('配置文件,查无此[{}]{}'.format(section, option))
            value = None
        finally:
            return value

    def _write(self, section, option, value):
        # 检查配置组是否不存在，不存在则添加配置组
        if not self.cfg.has_section(section):
            self.cfg.add_section(section)
            self.lgo.info('新增[{}]'.format(section))
        self.cfg.set(section, option, value)
        self.log.info('设置[section]{}={}'.format(option, value))
        self.cfg.write(open(cfg_path, 'w'))

    def _remove(self, section, option):
        # 检查配置组是否存在，存在则删除配置项，否则不操作
        if self.cfg.has_section(section):
            self.cfg.remove_option(section, option)
            self.log.info('删除[{}]{}'.format(section, option))
            self.cfg.write(open(cfg_path, 'w'))
        else:
            pass

    def restore(self):
        backup = ''
        with open(cfg_path, mode='w', encoding='utf-8') as f:
            f.write(backup)
        self.log.info('已恢复默认配置')
