
#source -- https://www.youtube.com/watch?v=uy4TPngK-8c

from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.orm import sessionmaker, declarative_base



DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/postgres'


engine = create_engine(DATABASE_URL)
conn  = engine.raw_connection() 
cursor = conn.cursor()

#cursor.execute('select * from task_list ;')
#df = pd.read_sql_query('select * from tasks ;', con=engine)
#res = cursor.fetchall()
#print(df)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


