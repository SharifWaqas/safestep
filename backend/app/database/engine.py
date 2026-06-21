from sqlalchemy import create_engine
from backend.app import config

db_host = config.DB_HOST
db_name = config.DB_NAME
db_password = config.DB_PASSWORD
db_port = str(config.DB_PORT)
db_user = config.DB_USER
db_url = "postgresql://" + db_user + ":" +db_password +"@" + db_host +":"+db_port +"/"+db_name


engine = create_engine(db_url)