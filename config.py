import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Colors:
    primary: str
    secondary: str

@dataclass
class Theme:
    colors: Colors

    @classmethod
    def from_dict(cls, d: dict) -> "Theme":
        return cls(colors=Colors(**d["colors"]))

@dataclass
class Config:
    theme: Theme

    @classmethod
    def load_file(cls, filepath: str | Path) -> "Config":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(theme=Theme.from_dict(data["theme"]))
        except:
            return None