from src.config.app_settings import DevelopmentSettings, TestSettings, ProductionSettings
from fastapi.logger import logger


def get_app_settings_by_mode(mode: str):

    mode_settings = {
        "development": DevelopmentSettings(),
        "test": TestSettings(),
        "production": ProductionSettings()
    }

    try:
        return mode_settings[mode]
    except KeyError:
        logger.error('Failed to load environment variables, app mode not found!. Setting to development...')
        return "development"