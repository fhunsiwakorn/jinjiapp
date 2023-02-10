from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:@localhost:3306/jinjidb"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://jinjidb:3wVrCP758y78@34.171.17.55/jinjidb?unix_socket=/cloudsql/jnjiproject:apijinji-test"

# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:pvbjIGofFHcXHc4jbhCX@containers-us-west-121.railway.app:7174/railway"
SQLALCHEMY_DATABASE_URL = "mysql://root:pvbjIGofFHcXHc4jbhCX@containers-us-west-121.railway.app:7174/railway"
engine = create_engine(SQLALCHEMY_DATABASE_URL,  pool_size=100,
                       max_overflow=15, pool_pre_ping=True, pool_recycle=60*60)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()
