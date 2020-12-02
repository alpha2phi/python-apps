#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
# Script to import fro csv files to database tables

import os
import argparse
import pandas as pd

from impala.dbapi import connect
from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.types import String
from impala.util import as_pandas



def csv_2_db(csv_file, table_name):
    load_dotenv(find_dotenv())
    DB_HOST = os.getenv("DB_HOST")
    DB = os.getenv("DB")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")

    print(f"Host: {DB_HOST}")
    print(f"DB: {DB}")
    print(f"DB_PORT: {DB_PORT}")

    def get_conn():
        return connect(host=DB_HOST,
                    port=int(DB_PORT),
                    use_ssl=True,
                    auth_mechanism='GSSAPI',
                    kerberos_service_name='impala',
                    database=DB,
                    )

    engine = create_engine('impala://', creator=get_conn)
    inspector = inspect(engine)
    dtypes = {}
    for column in inspector.get_columns(table_name, schema=DB):
        # print("Column: %s" % column)
        dtypes[column['name']] = column['type']
    print(dtypes)
    df = pd.read_excel(csv_file) #, dtype=schema)

    print("\nCSV info")
    print("*" * 10)
    print(df.info())
    print(df.head(10))

    # Save to db
    df.to_sql(table_name, engine, if_exists="append", chunksize=500, index=False, dtype=dtypes)

    # Validation
    print(f"\nTotal records in {csv_file} - {len(df)}")
    for c in df.columns:
        print(f"{c} - {df[c].nunique()}")

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    df1 = as_pandas(cursor)
    print(f"\nTotal records in {table_name} - {len(df1)}")
    for c in df1.columns:
        print(f"{c} - {df1[c].nunique()}")

    cursor.close()
    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file")
    parser.add_argument("table_name")
    args = parser.parse_args()
    print(f"Import from {args.csv_file} to {args.table_name}")
    csv_2_db(args.csv_file, args.table_name)


if __name__ == "__main__":
    main()
