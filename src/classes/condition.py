from fhir.resources.condition import Condition as fhirCondition


class Condition:
    def __init__(self) -> None:
        self.create_types = [
            "CREATE TYPE condition_status_type as ENUM('active', 'recurrence', 'relapse', 'inactive', 'remission', 'resolved', 'unknown')",
            "CREATE TYPE condition_verification_type as ENUM('unconfirmed', 'provisional', 'differential', 'confirmed', 'refuted')",
        ]

        self.create_table = """
            CREATE TABLE condition (
                id SERIAL PRIMARY KEY,
                condition_id CHAR(36) UNIQUE,
                patient_id CHAR(36),
                encounter_id CHAR(36),
                status condition_status_type,
                verification_status condition_verification_type,
                category VARCHAR(500),
                code_id VARCHAR(255),
                code_display VARCHAR(255),
                onset_timestamp TIMESTAMPTZ,
                abatement_timestamp TIMESTAMPTZ,
                recorded_timestamp TIMESTAMPTZ,
                CONSTRAINT fk_encounter FOREIGN KEY(encounter_id)
                            REFERENCES encounter(encounter_id)
                            ON UPDATE CASCADE ON DELETE CASCADE
            )
        """

    def from_fhir(self, patient_id: str, fhir_condition: fhirCondition):
        """Creates a dict of fields required for the condition table from the fhir condition object
        """
        condition_dict = dict(
            condition_id=fhir_condition.id,
            patient_id=patient_id,
            encounter_id=fhir_condition.encounter.reference.replace("urn:uuid:", ""),
            status=fhir_condition.clinicalStatus.coding[0].code,
            verification_status=fhir_condition.verificationStatus.coding[0].code,
            category=", ".join([cat.coding[0].code for cat in fhir_condition.category])
            or None,
            code_id=fhir_condition.code.coding[0].code,
            code_display=fhir_condition.code.text,
            onset_timestamp=fhir_condition.onsetDateTime,
            abatement_timestamp=fhir_condition.abatementDateTime,
            recorded_timestamp=fhir_condition.recordedDate,
            effective_timestamp=fhir_condition.recordedDate,
        )
        return condition_dict

    def to_insert_query(self):
        return """
               INSERT INTO condition (condition_id, patient_id, encounter_id, status, verification_status, category, code_id, code_display, onset_timestamp, abatement_timestamp, recorded_timestamp)
               VALUES (%(condition_id)s, %(patient_id)s, %(encounter_id)s, %(status)s, %(verification_status)s, %(category)s, %(code_id)s, %(code_display)s, %(onset_timestamp)s, %(abatement_timestamp)s, %(recorded_timestamp)s)
               """
