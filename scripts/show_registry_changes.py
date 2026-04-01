import json

from src.config.settings import get_settings


def main():
    settings = get_settings()

    with open(settings.registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    changes = registry.get("changes", {})

    print("Registry change summary:\n")
    for key in ["new", "modified", "deleted", "unchanged"]:
        items = changes.get(key, [])
        print(f"{key.upper()} ({len(items)}):")
        for item in items:
            print(f"  - {item}")
        print()


if __name__ == "__main__":
    main()