from fhir.resources.humanname import HumanName


class Name:
    def __init__(self) -> None:
        self.create_types = [
            "CREATE TYPE name_use_type AS ENUM('usual', 'official', 'temp', 'nickname', 'anonymous', 'old', 'maiden');"
        ]

        self.create_table = """
            CREATE TABLE name (
                id SERIAL PRIMARY KEY,
                patient_id CHAR(36),
                start_timestamp TIMESTAMPTZ,
                end_timestamp TIMESTAMPTZ,
                given VARCHAR(255),
                family VARCHAR(255),
                prefix VARCHAR(100),
                text VARCHAR(255),
                use name_use_type,
                CONSTRAINT fk_patient FOREIGN KEY(patient_id)
                    REFERENCES patient(id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
        """

    def from_fhir(self, patient_id: str, fhir_names: HumanName):
        """Creates a list of dicts of fields required for the names table from the fhir name object
        """
        names = []
        for name in fhir_names:
            name_dict = dict(
                patient_id=patient_id,
                start_timestamp=name.period.start if name.period else None,
                end_timestamp=name.period.start if name.period else None,
                family=name.family,
                # In the data sample only one given and prefix present but schema indicates that it is
                # a list. For the purpose of exercise, concatinate the attrs but if there was a need,
                # another table should be created with a many to many relationship between this table
                # and the given name/ prefix tables
                given=", ".join(name.given),
                prefix=", ".join(name.prefix) if name.prefix else None,
                text=name.text,
                use=name.use,
            )
            names.append(name_dict)
        return names

    def to_insert_query(self):
        return """
               INSERT INTO name (patient_id, start_timestamp, end_timestamp, family, given, prefix, text, use)
               VALUES (%(patient_id)s, %(start_timestamp)s, %(end_timestamp)s, %(family)s, %(given)s, %(prefix)s, %(text)s, %(use)s)
            """
