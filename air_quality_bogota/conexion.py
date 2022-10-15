from sqlalchemy import create_engine
import psycopg2
import pandas as pd
import io
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(f'postgresql+psycopg2://postgres:pg123@127.0.0.1:5432/airQuality')

def new_model(df, name_model):
    df = df.rename_axis('id').reset_index()
    df['id'] = df.index+1
    df.head(0).to_sql(name_model, engine, if_exists='replace', index=False) #drops old table and creates new empty table


    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, name_model, null="") # null values become ''
    conn.commit()