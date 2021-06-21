from dynaconf import Dynaconf

settings = Dynaconf(envvar_prefix="APPOINTMENT", load_dotenv=True)
