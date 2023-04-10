import datetime
import json

import pytest
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
from fhir.resources import construct_fhir_element


@pytest.fixture
def bundle():
    f = open(
        "tests/files/Leonardo412_Schuppe920_10bf6da8-ffa1-6913-a119-726634be754c.json"
    )
    f = json.load(f)
    bundle = construct_fhir_element("Bundle", f)
    return bundle


@pytest.fixture
def patient(bundle):
    patient = next(
        entry.resource
        for entry in bundle.entry
        if entry.resource.resource_type == "Patient"
    )
    return patient


@pytest.fixture
def fhir_encounter(bundle):
    encounter = next(
        entry.resource
        for entry in bundle.entry
        if entry.resource.resource_type == "Encounter"
    )
    return encounter


@pytest.fixture
def fhir_observation(bundle):
    obsrvation = next(
        entry.resource
        for entry in bundle.entry
        if entry.resource.resource_type == "Observation"
    )
    return obsrvation


@pytest.fixture
def fhir_condition(bundle):
    condition = next(
        entry.resource
        for entry in bundle.entry
        if entry.resource.resource_type == "Condition"
    )
    return condition


def tests_from_fhir_patient(patient):
    patient_cls = Patient()
    patient_dict = patient_cls.from_fhir(patient)
    assert patient_dict["id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert patient_dict["birth_date"] == datetime.date(1946, 12, 13)
    assert patient_dict["deceased"] is False
    assert patient_dict["deceased_timestamp"] is None
    assert patient_dict["race"] == "white"
    assert patient_dict["ethnicity"] == "not hispanic or latino"
    assert patient_dict["birth_sex"] == "M"
    assert patient_dict["birth_place"] == "Amherst, Massachusetts, US"
    assert patient_dict["mothers_maiden_name"] == "Georgann131 Gaylord332"
    assert round(patient_dict["disability_adjusted_life_years"], 2) == 0.14
    assert round(patient_dict["quality_adjusted_life_years"], 2) == 73.86
    assert patient_dict["gender"] == "male"
    assert patient_dict["marital_status"] == "M"
    assert patient_dict["multiple_births"] is True
    assert patient_dict["multiple_births_count"] == 3


def tests_from_fhir_addresses(patient):
    address_cls = Address()
    addresses = address_cls.from_fhir(patient.id, patient.address)
    assert isinstance(addresses, list)
    # Returns list of dicts but it is known that patient has one address
    address = addresses[0]
    assert address["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert address["city"] == "Taunton"
    assert address["country"] == "US"
    assert address["district"] is None
    assert address["line"] == "848 Miller Ville"
    assert address["postal_code"] is None
    assert address["state"] == "MA"
    assert address["text"] is None
    assert address["start_timestamp"] is None
    assert address["end_timestamp"] is None
    assert address["use"] is None
    assert round(address["lat"], 2) == 41.92
    assert round(address["lon"], 2) == -71.1


def tests_from_fhir_names(patient):
    name_cls = Name()
    names = name_cls.from_fhir(patient.id, patient.name)
    assert isinstance(names, list)
    name = names[0]
    assert name["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert name["start_timestamp"] is None
    assert name["end_timestamp"] is None
    assert name["family"] == "Schuppe920"
    assert name["given"] == "Leonardo412"
    assert name["prefix"] == "Mr."
    assert name["text"] is None
    assert name["use"] == "official"


def tests_from_fhir_languages(patient):
    language = Language()
    languages = language.from_fhir(patient.id, patient.communication)
    assert isinstance(languages, list)
    lang = languages[0]
    assert lang["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert lang["language_id"] == "en-US"


def tests_from_fhir_telecom(patient):
    telecom = Telecom()
    communications = telecom.from_fhir(patient.id, patient.telecom)
    assert isinstance(communications, list)
    comm = communications[0]
    assert comm["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert comm["start_timestamp"] is None
    assert comm["end_timestamp"] is None
    assert comm["rank"] is None
    assert comm["system"] == "phone"
    assert comm["use"] == "home"
    assert comm["value"] == "555-294-9369"


def tests_from_fhir_identifiers(patient):
    identifier = Identifier()
    identifiers = identifier.from_fhir(patient.id, patient.identifier)
    assert isinstance(identifiers, list)
    assert len(identifiers) == 4
    idf = identifiers[0]
    assert idf["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert idf["assigner"] is None
    assert idf["start_timestamp"] is None
    assert idf["end_timestamp"] is None
    assert idf["system"] == "http://hospital.smarthealthit.org"
    assert idf["type_code"] == "MR"
    assert idf["type_display"] == "Medical Record Number"
    assert idf["use"] is None
    assert idf["value"] == "10bf6da8-ffa1-6913-a119-726634be754c"


def tests_from_fhir_encounter(patient, fhir_encounter):
    cls_encounter = Encounter()
    _, encounter = cls_encounter.from_fhir(patient.id, fhir_encounter)
    assert encounter["encounter_id"] == fhir_encounter.id
    assert encounter["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert encounter["class_fhir"] == "AMB"
    assert encounter["start_timestamp"] == datetime.datetime(
        1965, 2, 5, 6, 16, 52, tzinfo=datetime.timezone.utc
    )
    assert encounter["end_timestamp"] == datetime.datetime(
        1965, 2, 5, 6, 31, 52, tzinfo=datetime.timezone.utc
    )
    assert encounter["service_provider"] == "STEWARD MEDICAL GROUP, INC"
    assert encounter["status"] == "finished"
    assert encounter["hospitalization_code"] is None
    assert encounter["hospitalization_text"] is None
    assert encounter["type"] == "General examination of patient (procedure)"


def tests_from_fhir_participants(patient, fhir_encounter):
    cls_encounter_participant = EncounterParticipant()
    participants, _ = cls_encounter_participant.from_fhir(
        patient.id, fhir_encounter.id, fhir_encounter.participant
    )
    assert isinstance(participants, list)
    participant = participants[0]
    assert participant["name"] == "Dr. Dwayne786 Leannon79"
    assert (
        participant["reference"]
        == "Practitioner?identifier=http://hl7.org/fhir/sid/us-npi|9999913759"
    )


def tests_from_fhir_encounter_participants(patient, fhir_encounter):
    cls_encounter_participant = EncounterParticipant()
    _, encounter_participants = cls_encounter_participant.from_fhir(
        patient.id, fhir_encounter.id, fhir_encounter.participant
    )
    assert isinstance(encounter_participants, list)
    participant = encounter_participants[0]
    assert participant["encounter_id"] == fhir_encounter.id
    assert participant["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert participant["text"] == "primary performer"
    assert participant["start_timestamp"] == datetime.datetime(
        1965, 2, 5, 6, 16, 52, tzinfo=datetime.timezone.utc
    )
    assert participant["end_timestamp"] == datetime.datetime(
        1965, 2, 5, 6, 31, 52, tzinfo=datetime.timezone.utc
    )


def tests_from_fhir_observation(patient, fhir_observation):
    cls_observation = Observation()
    observation = cls_observation.from_fhir(patient.id, fhir_observation)
    assert observation["observation_id"] == "f0a287bf-7279-c747-6e39-d0e24b2b4038"
    assert observation["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert observation["encounter_id"] == "72f28f70-5a53-b3d4-6afe-43a399947004"
    assert observation["status"] == "final"
    assert observation["category"] == "vital-signs"
    assert observation["code_id"] == "8302-2"
    assert observation["code_display"] == "Body Height"
    assert observation["effective_timestamp"] == datetime.datetime(
        2012, 3, 9, 6, 16, 52, tzinfo=datetime.timezone.utc
    )
    assert observation["issued"] == datetime.datetime(
        2012, 3, 9, 6, 16, 52, 615000, tzinfo=datetime.timezone.utc
    )


def tests_from_fhir_condition(patient, fhir_condition):
    cls_condition = Condition()
    condition = cls_condition.from_fhir(patient.id, fhir_condition)
    assert condition["condition_id"] == "793afc36-e876-41db-489c-51771becb426"
    assert condition["patient_id"] == "10bf6da8-ffa1-6913-a119-726634be754c"
    assert condition["encounter_id"] == "90f530e3-7aea-5889-e5af-9ae0bb8711d8"
    assert condition["status"] == "active"
    assert condition["verification_status"] == "confirmed"
    assert condition["category"] == "encounter-diagnosis"
    assert condition["code_id"] == "224299000"
    assert condition["code_display"] == "Received higher education (finding)"
    assert condition["onset_timestamp"] == datetime.datetime(
        1965, 2, 5, 7, 13, 9, tzinfo=datetime.timezone.utc
    )
    assert condition["abatement_timestamp"] is None
    assert condition["recorded_timestamp"] == datetime.datetime(
        1965, 2, 5, 7, 13, 9, tzinfo=datetime.timezone.utc
    )
    assert condition["effective_timestamp"] == datetime.datetime(
        1965, 2, 5, 7, 13, 9, tzinfo=datetime.timezone.utc
    )
