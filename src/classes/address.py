class Address:
    def __init__(self) -> None:
        self.create_types = [
            "CREATE TYPE address_type AS ENUM('postal', 'physical', 'both');",
            "CREATE TYPE address_use_type AS ENUM('home', 'work', 'temp', 'old');",
        ]
        self.create_table = """
            CREATE TABLE address (
                id SERIAL PRIMARY KEY,
                patient_id CHAR(36),
                city VARCHAR(255),
                country VARCHAR(255),
                district VARCHAR(255),
                line VARCHAR(255),
                postal_code VARCHAR(10),
                state VARCHAR(2),
                text VARCHAR(255),
                type address_type,
                start_timestamp TIMESTAMPTZ,
                end_timestamp TIMESTAMPTZ,
                use address_use_type,
                lat DECIMAL,
                lon DECIMAL,
                CONSTRAINT fk_patient FOREIGN KEY(patient_id)
                    REFERENCES patient(id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
        """

    def from_fhir(self, patient_id, fhir_addresses):
        addresses = []
        for address in fhir_addresses:
            lat = next(
                (
                    coord.valueDecimal
                    for coord in address.extension[0].extension
                    if coord.url == "latitude"
                ),
                None,
            )
            lon = next(
                (
                    coord.valueDecimal
                    for coord in address.extension[0].extension
                    if coord.url == "longitude"
                ),
                None,
            )
            address_dict = dict(
                patient_id=patient_id,
                city=address.city,
                country=address.country,
                district=address.district,
                line=' ,'.join(address.line),
                postal_code=address.postalCode,
                state=address.state,
                text=address.text,
                type=address.type,
                start_timestamp=address.period.start if address.period else None,
                end_timestamp=address.period.end if address.period else None,
                use=address.use,
                lat=float(lat) if lat else None,
                lon=float(lon) if lon else None,
            )
            addresses.append(address_dict)
        return addresses

    def to_insert_query(self):
        return """
               INSERT INTO address (patient_id, city, country, district, line, postal_code, state, text, type, start_timestamp, end_timestamp, use, lat, lon)
               VALUES (%(patient_id)s, %(city)s, %(country)s, %(district)s, %(line)s, %(postal_code)s, %(state)s, %(text)s, %(type)s, %(start_timestamp)s, %(end_timestamp)s, %(use)s, %(lat)s, %(lon)s)
               """
