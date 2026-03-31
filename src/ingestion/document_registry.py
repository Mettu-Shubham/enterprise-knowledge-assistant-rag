import hashlib
import json
import os
from datetime import datetime


class DocumentRegistry:

    def __init__(self, registry_path="data/document_registry.json"):
        self.registry_path = registry_path
        self._ensure_parent_dir()

    def _ensure_parent_dir(self):
        parent = os.path.dirname(self.registry_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

    def load(self):
        if not os.path.exists(self.registry_path):
            return {"documents": []}

        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, documents):
        payload = {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "documents": documents,
        }
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def build_entry(self, absolute_path, root_path):
        stat = os.stat(absolute_path)
        relative_path = os.path.relpath(absolute_path, root_path).replace("\\", "/")
        domain = relative_path.split("/")[0] if "/" in relative_path else "uncategorized"
        file_name = os.path.basename(absolute_path)
        extension = os.path.splitext(file_name)[1].lower().lstrip(".")

        return {
            "source": file_name,
            "domain": domain,
            "relative_path": relative_path,
            "absolute_path": absolute_path,
            "file_type": extension,
            "file_size": stat.st_size,
            "last_modified": stat.st_mtime,
            "fingerprint": self._fingerprint(absolute_path),
        }

    def _fingerprint(self, absolute_path):
        hasher = hashlib.sha256()
        with open(absolute_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()