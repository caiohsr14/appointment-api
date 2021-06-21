from dynaconf import Dynaconf

settings = Dynaconf(envvar_prefix="BILLING", load_dotenv=True)
