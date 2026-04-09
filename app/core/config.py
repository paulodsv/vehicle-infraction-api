from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    INFOSIMPLES_TOKEN: str
    INFOSIMPLES_CRYPTO_KEY: str

    GOV_CPF: str
    GOV_SENHA: str
    MANDACARI_CNPJ: str
    MAVI_CNPJ: str
    TRANSP_MANDACARI_CNPJ: str
    RELOG_CNPJ: str

    INFOSIMPLES_INFRACTIONS_URL: str
    INFOSIMPLES_DETAILS_URL : str

    model_config = {"env_file": ".env"}

settings = Settings()