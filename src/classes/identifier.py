class Identifier:
    def __init__(self) -> None:
        self.create_types = [
            "CREATE TYPE id_use_type AS ENUM('home', 'work', 'temp', 'old', 'mobile');",
        ]

        self.create_table = """
            CREATE TABLE identifier (
                id SERIAL PRIMARY KEY,
                patient_id CHAR(36),
                assigner VARCHAR(255),
                start_timestamp TIMESTAMPTZ,
                end_timestamp TIMESTAMPTZ,
                system TEXT,
                type_code VARCHAR(10),
                type_display VARCHAR(255),
                use id_use_type,
                value VARCHAR(255),
                CONSTRAINT fk_patient FOREIGN KEY(patient_id)
                    REFERENCES patient(id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
        """

    def from_fhir(self, patient_id, fhir_identifiers):
        identifiers = []
        for identifier in fhir_identifiers:
            # It looks like MR type entry is duped where one of the entries don't have type id
            type_code = identifier.type.coding[0].code if identifier.type else None
            if not type_code:
                continue
            identifier_dict = dict(
                patient_id=patient_id,
                assigner=identifier.assigner,
                start_timestamp=identifier.period.start if identifier.period else None,
                end_timestamp=identifier.period.end if identifier.period else None,
                system=identifier.system,
                type_code=type_code,
                type_display=identifier.type.coding[0].display if identifier.type else None,
                use=identifier.use,
                value=identifier.value,
            )
            identifiers.append(identifier_dict)
        return identifiers

    def to_insert_query(self):
        return """
               INSERT INTO identifier (patient_id, assigner, start_timestamp, end_timestamp, system, type_code, type_display, use, value) 
               VALUES (%(patient_id)s, %(assigner)s, %(start_timestamp)s, %(end_timestamp)s, %(system)s, %(type_code)s, %(type_display)s, %(use)s, %(value)s)
               """
