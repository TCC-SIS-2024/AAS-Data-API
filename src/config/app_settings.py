from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    APP_MODE: str

    model_config = SettingsConfigDict(
        env_file='.env'
    )

class DevelopmentSettings(AppSettings):

    model_config = SettingsConfigDict(
        env_file='.env.development'
    )


class TestSettings(AppSettings):
    model_config = SettingsConfigDict(
        env_file='.env.test'
    )


class ProductionSettings(AppSettings):
    model_config = SettingsConfigDict(
        env_file='.env.production'
    )

class EnvironmentVariables:
    vars: AppSettings

    def __new__(cls, vars: AppSettings):
        cls.vars = vars
        return cls



