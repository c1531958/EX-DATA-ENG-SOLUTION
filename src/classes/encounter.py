class Encounter:
    def __init__(self) -> None:
        self.create_types = [
            "CREATE TYPE encounter_status_type AS ENUM('planned', 'arrived', 'in-progress', 'onleave', 'finished', 'cancelled')"
        ]

        self.create_table = """
            CREATE TABLE encounter (
                encounter_id CHAR(36) PRIMARY KEY,
                patient_id CHAR(36),
                class_fhir VARCHAR(255),
                start_timestamp TIMESTAMPTZ,
                end_timestamp TIMESTAMPTZ,
                service_provider VARCHAR(255),
                status encounter_status_type,
                hospitalization_code INT,
                hospitalization_text VARCHAR(255),
                type VARCHAR(255),
                CONSTRAINT fk_encounter FOREIGN KEY(patient_id)
                            REFERENCES patient(id)
                            ON UPDATE CASCADE ON DELETE CASCADE
            )
        """

    def from_fhir(self, patient_id, fhir_encounter):
        # Use org_names to keep track of unique orgs between provdier and locations
        orgs, org_names = [], set()
        hospitalization = (
            fhir_encounter.hospitalization.dischargeDisposition.coding[0]
            if fhir_encounter.hospitalization
            else None
        )
        encounter = dict(
            encounter_id=fhir_encounter.id,
            patient_id=patient_id,
            class_fhir=fhir_encounter.class_fhir.code,
            start_timestamp=fhir_encounter.period.start if fhir_encounter.period else None,
            end_timestamp=fhir_encounter.period.end if fhir_encounter.period else None,
            service_provider=fhir_encounter.serviceProvider.display,
            status=fhir_encounter.status,
            hospitalization_code=int(hospitalization.code) if hospitalization else None,
            hospitalization_text=hospitalization.display if hospitalization else None,
            type=fhir_encounter.type[0].text,
        )
        if service_provider := fhir_encounter.serviceProvider:
            orgs.append(
                dict(
                    display_name=service_provider.display,
                    type=service_provider.reference.split("?")[0].lower(),
                    reference=service_provider.reference,
                )
            )
            org_names.add(service_provider.display)

        for location in fhir_encounter.location:
            location_name = location.location.display
            if location_name not in org_names:
                orgs.append(
                    dict(
                        display_name=location_name,
                        type="location",
                        reference=location.location.reference,
                    )
                )

        return orgs, encounter

    def to_insert_query(self):
        return """
               INSERT INTO encounter (encounter_id, patient_id, class_fhir, start_timestamp, end_timestamp, service_provider, status, hospitalization_code, hospitalization_text)
               VALUES (%(encounter_id)s, %(patient_id)s, %(class_fhir)s, %(start_timestamp)s, %(end_timestamp)s, %(service_provider)s, %(status)s, %(hospitalization_code)s, %(hospitalization_text)s)
               """
