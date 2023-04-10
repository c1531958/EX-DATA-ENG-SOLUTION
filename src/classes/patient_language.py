class PatientLanguage:
    def __init__(self) -> None:
        self.create_types = []
        self.create_table = """
            CREATE TABLE patient_language (
                patient_id CHAR(36),
                language_id VARCHAR(5),
                PRIMARY KEY (patient_id, language_id),
                CONSTRAINT fk_patient FOREIGN KEY(patient_id) REFERENCES patient(id),
                CONSTRAINT fk_language FOREIGN KEY(language_id) REFERENCES language(id)
            )
        """
