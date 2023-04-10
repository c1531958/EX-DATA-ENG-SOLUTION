import os
import create_tables as create_tables
import file_importer as file_importer


def main():
    """Runs bot table creation and all data insertion
    """
    create_tables.create_tables()
    data_path = f"{os.getcwd()}/data"
    file_importer.main(data_path)


if __name__ == "__main__":
    main()
