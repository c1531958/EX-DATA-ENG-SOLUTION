class EncounterParticipant:
    def __init__(self) -> None:
        self.create_types = []
        self.create_table = """
            CREATE TABLE encounter_participant (
                encounter_id CHAR(36),
                participant_id INT,
                PRIMARY KEY (encounter_id, participant_id),
                patient_id CHAR(36),
                text VARCHAR(255),
                start_timestamp TIMESTAMPTZ,
                end_timestamp TIMESTAMPTZ,
                CONSTRAINT fk_encounter FOREIGN KEY(encounter_id) REFERENCES encounter(encounter_id),
                CONSTRAINT fk_participant FOREIGN KEY(participant_id) REFERENCES participant(id)
            )
        """

    def from_fhir(self, patient_id, encounter_id, fhir_participants):
        participants, encounter_participants = [], []
        # TODO extract type from the reference string
        for participant in fhir_participants:
            participant_dict = dict(
                name=participant.individual.display,
                reference=participant.individual.reference,
            )
            participants.append(participant_dict)

            # Won't have participant id here as that will be retrieved on insert of participants
            encounter_participant_dict = dict(
                encounter_id=encounter_id,
                patient_id=patient_id,
                text=participant.type[0].text,
                start_timestamp=participant.period.start if participant.period else None,
                end_timestamp=participant.period.end if participant.period else None,
            )
            encounter_participants.append(encounter_participant_dict)
        return participants, encounter_participants
