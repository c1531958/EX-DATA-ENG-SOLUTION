import os

import psycopg


class PostgresUtils:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, db_name=None):
        self.connection = psycopg.connect(
            dbname=os.environ.get("DB_NAME") or db_name,
            user=os.environ.get("USERNAME"),
            password=os.environ.get("PASSWORD"),
            port=os.environ.get("PORT"),
            host=os.environ.get("HOST"),
        )

    def connect_server(self):
        self.connection = psycopg.connect(
            user=os.environ.get("USERNAME"),
            password=os.environ.get("PASSWORD"),
            port=os.environ.get("PORT"),
            host=os.environ.get("HOST"),
            autocommit=True,
        )

    def get_cursor(self):
        self.cursor = self.connection.cursor()

    def execute(self, sql, record):
        self.cursor.execute(sql, record)
        self.connection.commit()

    def execute_many(self, sql, records):
        self.cursor.executemany(sql, records)
        self.connection.commit()

    def insert_languages(self, languages):
        self.cursor.executemany(
            """
            INSERT INTO language (id, language)
            VALUES (%s, %s)
            """,
            languages,
        )
        self.connection.commit()

    def insert_identifiers(self, identifiers):
        self.cursor.executemany(
            """
            INSERT INTO identifier (patient_id, assigner, start_timestamp, end_timestamp, system, type_code, type_display, use, value) 
            VALUES (%(patient_id)s, %(assigner)s, %(start_timestamp)s, %(end_timestamp)s, %(system)s, %(type_code)s, %(type_display)s, %(use)s, %(value)s)
            """,
            identifiers,
        )
        self.connection.commit()

    def insert_participants(self, participants, encounter_participants):
        for i, participant in enumerate(participants):
            self.cursor.execute(
                """
                WITH input_rows(name, reference) AS (
                VALUES
                    (%(name)s, %(reference)s)
                )
                , ins AS (
                    INSERT INTO participant (name, reference)
                    SELECT * FROM input_rows
                    ON CONFLICT DO NOTHING
                    RETURNING id
                )
                SELECT 'i' AS source, id
                FROM   ins
                UNION  ALL
                SELECT 's' AS source, participant.id
                FROM input_rows
                JOIN participant USING (name);
                """,
                participant,
            )
            participant_id = self.cursor.fetchall()[0]
            encounter_participants[i]["participant_id"] = participant_id[1]

        # create the reference record
        self.connection.commit()
        self.cursor.executemany(
            """INSERT INTO encounter_participant (encounter_id, patient_id, participant_id, text, start_timestamp, end_timestamp)
               VALUES (%(encounter_id)s, %(patient_id)s, %(participant_id)s, %(text)s, %(start_timestamp)s, %(end_timestamp)s)
            """,
            encounter_participants,
        )
        self.connection.commit()


def get_connection():
    pg = PostgresUtils()
    pg.connect()
    pg.get_cursor()
    return pg
