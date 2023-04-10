class Observation:
    def __init__(self) -> None:
        self.create_types = [
            "CREATE TYPE observation_status_type as ENUM('registered', 'preliminary', 'final', 'amended', '+')"
        ]

        self.create_table = """
            CREATE TABLE observation (
                id SERIAL PRIMARY KEY,
                observation_id CHAR(36) UNIQUE,
                patient_id CHAR(36),
                encounter_id CHAR(36),
                status observation_status_type,
                category VARCHAR(255),
                code_id VARCHAR(255),
                code_display VARCHAR(255),
                effective_timestamp TIMESTAMPTZ,
                issued TIMESTAMPTZ,
                CONSTRAINT fk_encounter FOREIGN KEY(encounter_id)
                            REFERENCES encounter(encounter_id)
                            ON UPDATE CASCADE ON DELETE CASCADE
            )
        """

    def from_fhir(self, patient_id, fhir_observation):
        observation_dict = dict(
            observation_id=fhir_observation.id,
            patient_id=patient_id,  # or can be extracted from subject field TODO check
            encounter_id=fhir_observation.encounter.reference.replace("urn:uuid:", ""),
            status=fhir_observation.status,
            category=", ".join([cat.coding[0].code for cat in fhir_observation.category])
            or None,
            code_id=fhir_observation.code.coding[0].code,
            code_display=fhir_observation.code.text,
            effective_timestamp=fhir_observation.effectiveDateTime,
            issued=fhir_observation.issued,
        )
        return observation_dict

    def to_insert_query(self):
        return """
               INSERT INTO observation (observation_id, patient_id, encounter_id, status, category, code_id, code_display, effective_timestamp, issued)
               VALUES (%(observation_id)s, %(patient_id)s, %(encounter_id)s, %(status)s, %(category)s, %(code_id)s, %(code_display)s, %(effective_timestamp)s, %(issued)s)
               """
