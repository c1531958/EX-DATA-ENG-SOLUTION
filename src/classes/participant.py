class Participant:
    def __init__(self) -> None:
        self.create_types = []
        self.create_table = """
            CREATE TABLE participant (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                reference TEXT UNIQUE
            )
        """
