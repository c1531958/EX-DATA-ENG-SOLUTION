import json
import os

from fhir.resources import construct_fhir_element

from src.classes.address import Address
from src.classes.condition import Condition
from src.classes.encounter import Encounter
from src.classes.encounter_participant import EncounterParticipant
from src.classes.identifier import Identifier
from src.classes.language import Language
from src.classes.name import Name
from src.classes.observation import Observation
from src.classes.patient import Patient
from src.classes.telecom import Telecom
from src.utils import postgres_utils

address = Address()
condition = Condition()
encounter = Encounter()
encounter_participant = EncounterParticipant()
identifier = Identifier()
language = Language()
name = Name()
observation = Observation()
patient = Patient()
telecom = Telecom()


def main(data_path):
    pg = postgres_utils.get_connection()
    # iterate over files
    directory = os.fsencode(data_path)
    try:
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            f = open(f"{data_path}/{filename}")
            f = json.load(f)
            file_type = f.get("resourceType")
            if not file_type:
                print("Error no file type")
            bundle = construct_fhir_element(file_type, f)
            patient_id = None
            for entry in bundle.entry:
                resource = entry.resource
                if resource.resource_type == "Patient":
                    patient_id = resource.id
                    insert_patient_and_its_classes(pg, resource)
                elif resource.resource_type == "Encounter":
                    insert_encounter_and_its_classes(patient_id, pg, resource)
                elif resource.resource_type == "Observation":
                    insert_observation(patient_id, pg, resource)
                elif resource.resource_type == "Condition":
                    insert_condition(patient_id, pg, resource)

    except Exception as e:
        pg.connection.close()
        raise e


def insert_patient_and_its_classes(pg, resource):
    patient_id = resource.id
    patient_dict = patient.from_fhir(resource)
    patient_sql = patient.to_insert_query()
    pg.execute(patient_sql, patient_dict)
    # pg.insert_patient(patient_dict)
    # Insert addresses
    addresses = address.from_fhir(patient_id, resource.address)
    address_sql = address.to_insert_query()
    pg.execute_many(address_sql, addresses)
    # Insert names
    names = name.from_fhir(patient_id, resource.name)
    names_sql = name.to_insert_query()
    pg.execute_many(names_sql, names)
    # Insert patient languages
    patient_languages = language.from_fhir(patient_id, resource.communication)
    languages_sql = language.to_insert_query()
    pg.execute_many(languages_sql, patient_languages)
    # Insert communication methods
    comm_methods = telecom.from_fhir(patient_id, resource.telecom)
    telecom_sql = telecom.to_insert_query()
    pg.execute_many(telecom_sql, comm_methods)
    # Insert identifiers
    identifiers = identifier.from_fhir(patient_id, resource.identifier)
    identifier_sql = identifier.to_insert_query()
    pg.execute_many(identifier_sql, identifiers)


def insert_encounter_and_its_classes(patient_id, pg, resource):
    _, encounter_dict = encounter.from_fhir(patient_id, resource)
    # Insert encounter
    encounterm_sql = encounter.to_insert_query()
    pg.execute(encounterm_sql, encounter_dict)
    participants, encounter_participants = encounter_participant.from_fhir(
        patient_id, resource.id, resource.participant
    )

    pg.insert_participants(participants, encounter_participants)


def insert_observation(patient_id, pg, resource):
    observation_dict = observation.from_fhir(patient_id, resource)
    observationm_sql = observation.to_insert_query()
    pg.execute(observationm_sql, observation_dict)


def insert_condition(patient_id, pg, resource):
    condition_dict = condition.from_fhir(patient_id, resource)
    condition_sql = condition.to_insert_query()
    pg.execute(condition_sql, condition_dict)


if __name__ == "__main__":
    data_path = f"{os.getcwd()}/data"
    main(data_path)
