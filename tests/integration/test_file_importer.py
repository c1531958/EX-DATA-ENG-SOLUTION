import os

import src.create_tables as create_tables
import src.file_importer as file_importer


def test_file_importer(create_test_db):
    # First create tables
    create_tables.create_tables()
    # Import test files
    path = f"{os.getcwd()}/tests/files"
    file_importer.main(path)


def test_patient_records(test_db):
    patients = test_db.cursor.execute("SELECT * FROM patient").fetchall()
    assert len(patients) == 2


def test_address_records(test_db):
    addresses = test_db.cursor.execute("SELECT id FROM address").fetchall()
    assert len(addresses) == 2


def test_name_records(test_db):
    patients = test_db.cursor.execute("SELECT id FROM name").fetchall()
    assert len(patients) == 2


def test_indetifier_records(test_db):
    ids = test_db.cursor.execute("SELECT id FROM identifier").fetchall()
    assert len(ids) == 7


def test_language_patient_records(test_db):
    ids = test_db.cursor.execute("SELECT patient_id FROM patient_language").fetchall()
    assert len(ids) == 2


def test_telecom_records(test_db):
    ids = test_db.cursor.execute("SELECT id FROM telecom").fetchall()
    assert len(ids) == 2


def test_observation_records(test_db):
    ids = test_db.cursor.execute("SELECT id FROM observation").fetchall()
    assert len(ids) == 879


def test_encounter_records(test_db):
    ids = test_db.cursor.execute("SELECT encounter_id FROM encounter").fetchall()
    assert len(ids) == 46


def test_condition_records(test_db):
    ids = test_db.cursor.execute("SELECT id FROM condition").fetchall()
    assert len(ids) == 45


def test_participant_records(test_db):
    ids = test_db.cursor.execute("SELECT id FROM participant").fetchall()
    assert len(ids) == 4


def test_encounter_participant_records(test_db):
    ids = test_db.cursor.execute(
        "SELECT encounter_id FROM encounter_participant"
    ).fetchall()
    assert len(ids) == 46
