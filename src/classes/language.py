class Language:
    def __init__(self) -> None:
        self.create_types = []

        self.create_table = """
            CREATE TABLE language(
                id VARCHAR(5) PRIMARY KEY,
                language VARCHAR(255)
            )
        """

    def from_fhir(self, patient_id, fhir_communications):
        languages = []
        for communication in fhir_communications:
            lang_dict = dict(
                patient_id=patient_id,
                language_id=communication.language.coding[0].code,
            )
            languages.append(lang_dict)
        return languages

    def to_insert_query(self):
        return """
               INSERT INTO patient_language (patient_id, language_id)
               VALUES (%(patient_id)s, %(language_id)s)
               """
