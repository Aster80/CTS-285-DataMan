
import json
from pathlib import Path


class JsonFileStore:
    def __init__(self, file_path=None):
        if file_path is None:
            file_path = Path(__file__).resolve().parent.parent / "data" / "progress.json"

        self.file_path = Path(file_path)

    def load(self, player_id):
        if not self.file_path.exists():
            return {
                "attempts_used": 0,
                "completed": False,
                "status": "in_progress"
            }

        with open(self.file_path, "r") as file:
            data = json.load(file)

        return data.get(player_id, {
            "attempts_used": 0,
            "completed": False,
            "status": "in_progress"
        })

    def save(self, player_id, progress):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.file_path.exists():
            with open(self.file_path, "r") as file:
                data = json.load(file)
        else:
            data = {}

        data[player_id] = progress

        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def reset(self, player_id):
        self.save(player_id, {
            "attempts_used": 0,
            "completed": False,
            "status": "in_progress"
        })
