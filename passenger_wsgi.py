import os
from dotenv import load_dotenv
project_directory = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(project_directory, '.env'))

from collectorium.wsgi import application
