# import csv
# import os
# import sqlite3 as sql
# from sqlite3 import Error

from invoke import Exit, UnexpectedExit, task
from rich import print
from rich.panel import Panel

BASE_FOLDERS = "project4 network"


@task
def format(context, path=BASE_FOLDERS):
    context.run(f"python -m black {path}")


@task
def isort(context, path=BASE_FOLDERS):
    context.run(f"python -m isort {path}")


@task
def flake8(context, path=BASE_FOLDERS):
    context.run(f"python -m flake8 {path}")


@task
def checkall(context, path=BASE_FOLDERS):
    linters = [isort, flake8]
    failed = []
    for linter in linters:
        try:
            linter(context, path)
        except UnexpectedExit:
            failed.append(linter.__name__)
    if failed:
        msg = f"Linters failed: {', '.join(map(str.capitalize, failed))}"
        print(Panel(msg, style="yellow bold"))
        raise Exit(code=1)

# @task
# def convert_sqlite3_to_csv_file(context):
#     try:

#         # Connect to database
#         conn=sql.connect('db.sqlite3')
#         # Export data into CSV file
#         print(Panel(msg="Exporting data into CSV..........."), style="green"))
#         cursor = conn.cursor()
#         cursor.execute("select * from Employee")
#         with open("employee_data.csv", "w") as csv_file:
#             csv_writer = csv.writer(csv_file, delimiter="\t")
#             csv_writer.writerow([i[0] for i in cursor.description])
#             csv_writer.writerows(cursor)

#         dirpath = os.getcwd() + "/employee_data.csv"
#         # print "Data exported Successfully into {}".format(dirpath)

#     except Error as e:
#         print(e)

#     # Close database connection
#     finally:
#         conn.close()
