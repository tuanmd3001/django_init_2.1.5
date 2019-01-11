# -*- coding: utf-8 -*-
import importlib.util
import os

from constance import config

from app_themes.apps import AppThemesConfig


def get_template_dir():
    return os.path.join(config.THEME, config.THEME_TEMPLATE_DIR)


def get_template_base_dir():
    return os.path.join(config.THEME, config.THEME_TEMPLATE_DIR, AppThemesConfig.BASE_FILENAME)


def get_theme_configs():
    try:
        spec = importlib.util.spec_from_file_location('theme_config.py',
                                                      os.path.join('app_themes', 'themes', config.THEME,
                                                                   'theme_config.py'))
        theme_configs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(theme_configs)
        return theme_configs
    except:
        pass
    return None
