from src import create_tables


def exists_query(test_db, table_name):
    exists = test_db.cursor.execute(
        f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = '{table_name}'
            );"""
    ).fetchone()[0]
    return exists


def test_create_tables(create_test_db):
    create_tables.create_tables()


def test_patient_table_created(test_db):
    exists = exists_query(test_db, "patient")
    assert exists is True


def test_address_table_created(test_db):
    exists = exists_query(test_db, "address")
    assert exists is True


def test_language_table_created(test_db):
    exists = exists_query(test_db, "language")
    assert exists is True


def test_language_table_filled(test_db):
    language = test_db.cursor.execute(
        """
            SELECT language FROM language
            WHERE id = 'en-US';
        """
    ).fetchone()[0]
    assert language == "English"


def test_name_table_created(test_db):
    exists = exists_query(test_db, "name")
    assert exists is True


def test_telecom_table_created(test_db):
    exists = exists_query(test_db, "telecom")
    assert exists is True


def test_patient_language_table_created(test_db):
    exists = exists_query(test_db, "patient_language")
    assert exists is True


def test_identifier_table_created(test_db):
    exists = exists_query(test_db, "identifier")
    assert exists is True


def test_participant_table_created(test_db):
    exists = exists_query(test_db, "participant")
    assert exists is True


def test_encounter_participant_table_created(test_db):
    exists = exists_query(test_db, "encounter_participant")
    assert exists is True


def test_encounter_table_created(test_db):
    exists = exists_query(test_db, "encounter")
    assert exists is True


def test_observation_table_created(test_db):
    exists = exists_query(test_db, "observation")
    assert exists is True


def test_condition_table_created(test_db):
    exists = exists_query(test_db, "condition")
    assert exists is True
