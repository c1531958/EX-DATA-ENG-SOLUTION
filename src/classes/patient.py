class Patient:
    def __init__(self) -> None:
        self.create_types = [
            "CREATE TYPE gender_type AS ENUM('male', 'female', 'other', 'unknown');"
            "CREATE TYPE marital_status AS ENUM('M', 'S', 'A', 'D', 'I', 'L', 'C', 'P', 'T');"
        ]
        self.create_table = """
            CREATE TABLE patient (
                id CHAR(36) PRIMARY KEY,
                birth_date TIMESTAMPTZ,
                deceased BOOL,
                deceased_timestamp TIMESTAMPTZ,
                race VARCHAR(255),
                ethnicity VARCHAR(255),
                birth_sex VARCHAR(255),
                birth_place VARCHAR(255),
                mothers_maiden_name VARCHAR(255),
                gender gender_type,
                disability_adjusted_life_years FLOAT,
                quality_adjusted_life_years FLOAT,
                marital_status VARCHAR(255),
                multiple_births BOOL,
                multiple_births_count SMALLINT
            )
        """

    def from_fhir(self, fhir_patient):
        (
            race,
            ethnicity,
            birth_sex,
            birth_place,
            mothers_maiden_name,
            disability_y,
            quality_y,
        ) = self.get_human_attrs_from_extension(fhir_patient.extension)
        multiple_births = (
            fhir_patient.multipleBirthBoolean
            if fhir_patient.multipleBirthBoolean is not None
            else bool(fhir_patient.multipleBirthInteger)
        )
        patient_dict = dict(
            id=fhir_patient.id,
            birth_date=fhir_patient.birthDate,
            deceased=True if fhir_patient.deceasedDateTime else False,
            deceased_timestamp=fhir_patient.deceasedDateTime,
            race=race,
            ethnicity=ethnicity,
            birth_sex=birth_sex,
            birth_place=birth_place,
            mothers_maiden_name=mothers_maiden_name,
            disability_adjusted_life_years=disability_y,
            quality_adjusted_life_years=quality_y,
            gender=fhir_patient.gender,
            marital_status=fhir_patient.maritalStatus.text,
            multiple_births=multiple_births,
            multiple_births_count=fhir_patient.multipleBirthInteger,
        )

        return patient_dict

    def get_human_attrs_from_extension(self, extensions):
        (
            race,
            ethnicity,
            birth_sex,
            birth_place,
            mothers_maiden_name,
            disability_y,
            quality_y,
        ) = (None, None, None, None, None, None, None)
        for ext in extensions:
            if ext.url.endswith("-race"):
                race = ext.extension[0].valueCoding.display.lower()
            elif ext.url.endswith("-ethnicity"):
                ethnicity = ext.extension[0].valueCoding.display.lower()
            elif ext.url.endswith("-mothersMaidenName"):
                mothers_maiden_name = ext.valueString
            elif ext.url.endswith("-birthsex"):
                birth_sex = ext.valueCode
            elif ext.url.endswith("-birthPlace"):
                address = ext.valueAddress
                address_attrs = [
                    getattr(address, attr)
                    for attr in ["city", "state", "country"]
                    if getattr(address, attr)
                ]
                birth_place = ", ".join(address_attrs)
            elif ext.url.endswith("disability-adjusted-life-years"):
                disability_y = float(ext.valueDecimal)
            elif ext.url.endswith("quality-adjusted-life-years"):
                quality_y = float(ext.valueDecimal)
            else:
                print("Unknown attr")
        return (
            race,
            ethnicity,
            birth_sex,
            birth_place,
            mothers_maiden_name,
            disability_y,
            quality_y,
        )

    def to_insert_query(self):
        return """
            INSERT INTO patient (id, birth_date, deceased, deceased_timestamp, race, ethnicity, birth_sex, birth_place, mothers_maiden_name, disability_adjusted_life_years, quality_adjusted_life_years, gender, marital_status, multiple_births, multiple_births_count)
            VALUES (%(id)s, %(birth_date)s, %(deceased)s, %(deceased_timestamp)s, %(race)s, %(ethnicity)s, %(birth_sex)s, %(birth_place)s, %(mothers_maiden_name)s, %(disability_adjusted_life_years)s, %(quality_adjusted_life_years)s,%(gender)s, %(marital_status)s, %(multiple_births)s, %(multiple_births_count)s)
        """
