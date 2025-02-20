import certifi
import requests

from openai import OpenAI
from pymongo import MongoClient

from src.utils.utils import get_config, get_env

################# APP CONFIG #################

MODEL_CONFIG_PATH = "./src/config/model_config.yaml"
MODEL_CONFIG = get_config(MODEL_CONFIG_PATH)
DATA_CONFIG_PATH = "./src/config/data_config.yaml"
DATA_CONFIG = get_config(DATA_CONFIG_PATH)

#############################################


############### MONGODB VALUE ###############

MONGODB = DATA_CONFIG
API_KEY = get_env("API_KEY")
MONGODB_URI = get_env("MONGODB_URI")
CLIENT = MongoClient(
    MONGODB_URI,
    tls=True,
    tlsAllowInvalidCertificates=False,
    tlsCAFile=certifi.where(),
)  # Replace with your MongoDB URI
CONFIG_DATABASE = CLIENT[MONGODB["config_database"]]  # Database name
MODEL_DATABASE = CLIENT[MONGODB["model_database"]]  # Database name

#############################################
