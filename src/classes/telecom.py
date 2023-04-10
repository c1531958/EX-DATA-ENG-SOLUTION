class Telecom:
    def __init__(self) -> None:
        self.create_types = [
            "CREATE TYPE system_type AS ENUM('phone', 'fax', 'email', 'pager', 'url', 'sms', 'other');",
            "CREATE TYPE telecom_use_type AS ENUM('home', 'work', 'temp', 'old', 'mobile');",
        ]

        self.create_table = """
            CREATE TABLE telecom (
                id SERIAL PRIMARY KEY,
                patient_id CHAR(36),
                start_timestamp TIMESTAMPTZ,
                end_timestamp TIMESTAMPTZ,
                rank INT,
                system system_type,
                use telecom_use_type,
                value VARCHAR(255),
                CONSTRAINT fk_patient FOREIGN KEY(patient_id)
                    REFERENCES patient(id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
        """

    def from_fhir(self, patient_id, fhir_telecoms):
        comm_methods = []
        for com in fhir_telecoms:
            com_dict = dict(
                patient_id=patient_id,
                start_timestamp=com.period.start if com.period else None,
                end_timestamp=com.period.end if com.period else None,
                rank=com.rank,
                system=com.system,
                use=com.use,
                value=com.value,
            )
            comm_methods.append(com_dict)
        return comm_methods

    def to_insert_query(self):
        return """
               INSERT INTO telecom (patient_id, start_timestamp, end_timestamp, rank, system, use, value) 
               VALUES (%(patient_id)s, %(start_timestamp)s, %(end_timestamp)s, %(rank)s, %(system)s, %(use)s, %(value)s)
               """
