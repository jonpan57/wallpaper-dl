import os
import configparser
from .log import Log

dir_path = os.path.dirname(os.path.realpath(__file__))
cfg_path = os.path.join(dir_path, 'cfg.ini')
if not os.path.exists(cfg_path):  # 如果不存在配置文件，就自动创建一个并恢复默认配置
    os.mknod(cfg_path)


class Config:
    def __init__(self, section):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(cfg_path)
        self.section = section
        self.log = Log('config')
        if os.path.getsize(cfg_path) == 0:  # 配置文件为空，恢复默认配置
            self.restore()
            self.log.warning('配置文件为空')

    def config(self, option, value=None, convert='str'):  # 获取配置，同时可以修改配置
        if value:
            self._write(self.section, option, value)
        return self._get(self.section, option, convert)

    def _get(self, section, option, convert):
        try:
            if convert == 'str':
                value = self.cfg.get(section, option)
            elif convert == 'int':
                value = self.cfg.getint(section, option)
            elif convert == 'float':
                value = self.cfg.getfloat(section, option)
            elif convert == 'bool':
                value = self.cfg.getboolean(section, option)
            else:
                raise ValueError('Invalid typecast: ' + convert)
        except configparser.NoSectionError:
            self.log.error('配置文件，查无此[{}]'.format(section))
            value = None
        except configparser.NoOptionError:
            self.log.error('配置文件，查无此[{}]{}'.format(section, option))
            value = None
        except ValueError as e:
            if 'Invalid typecast'.find(str(e)):
                pass
            elif 'Not a boolean'.find(str(e)):
                pass
        finally:
            return value

    def _write(self, section, option, value):
        if not self.cfg.has_section(section):  # 检查配置组是否不存在，不存在则添加配置组
            self.cfg.add_section(section)
            self.lgo.info('已新增[{}]'.format(section))
        self.cfg.set(section, option, value)
        self.cfg.write(open(cfg_path, 'w'))
        self.log.info('已设置[{}}]{}={}'.format(section, option, value))

    def _remove(self, section, option):
        if self.cfg.has_section(section):  # 检查配置组是否存在，存在则删除配置项，否则不操作
            if self.cfg.remove_option(section, option):
                self.cfg.write(open(cfg_path, 'w'))
                self.log.info('已删除[{}]{}'.format(section, option))
            else:
                self.log.error('删除失败，查无此[{}]{}'.format(section, option))
        else:
            self.log.error('删除失败，查无此[{}]'.format(section))

    def restore(self):
        backup = ''
        with open(cfg_path, mode='w', encoding='utf-8') as f:
            f.write(backup)
        self.log.info('已恢复默认配置')
