import importlib

import psycopg

from src.classes.files.languages import bcp_47_languages
from src.utils.postgres_utils import PostgresUtils


def create_tables() -> None:
    """Creates all the tables in the PostgreSQL database"""
    pg = PostgresUtils()
    pg.connect()
    pg.get_cursor()
    try:
        # create tables one by one in order
        path = "src.classes"
        module_order = [
            "patient",
            "address",
            "name",
            "language",
            "patient_language",
            "telecom",
            "identifier",
            "encounter",
            "participant",
            "encounter_participant",
            "observation",
            "condition",
        ]
        # dynamically iterate over all the defined tables in the classes folder
        for filename in module_order:
            module_name = f"{path}.{filename}"
            class_neme = filename.title().replace("_", "")
            cls = getattr(importlib.import_module(module_name), class_neme)
            cls = cls()
            for enum_type_command in cls.create_types:
                pg.cursor.execute(enum_type_command)
            pg.cursor.execute(cls.create_table)
        # Prefill the language table
        pg.insert_languages(bcp_47_languages)

        # commit the changes and close the connection
        pg.connection.commit()
        pg.cursor.close()
    except (Exception, psycopg.DatabaseError) as error:
        pg.connection.close()
        raise error


if __name__ == "__main__":
    create_tables()
