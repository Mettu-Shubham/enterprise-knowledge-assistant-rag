from src.config.settings import get_settings
from src.ingestion.document_loader import DocumentLoader


def main():
    settings = get_settings()
    loader = DocumentLoader(settings.data_path, settings.registry_path)

    files = loader.discover_files()

    print(f"Discovered {len(files)} supported files in {settings.data_path}:\n")
    for file_path in files:
        print(file_path)


if __name__ == "__main__":
    main()