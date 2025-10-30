import sys
from pathlib import Path

homeDir = Path.home()
documentsDir = homeDir / "Documents"
programDir = documentsDir / "Digital Transmissions Log"
programDir.mkdir(parents=True, exist_ok=True)
stationsFile = programDir / "stations.txt"
netsFile = programDir / "nets.txt"
operatorsFile = programDir / "operators.txt"
logsFile = programDir / "logs.txt"
COLUMN_SEPARATOR = "⟺"
BODY_SEPARATOR = "⇒"

fileDictionary = {"stations":{"file":stationsFile},
                  "nets":{"file":netsFile},
                  "operators":{"file":operatorsFile},}

def returnFileValues(path: Path) -> list[str]:
    return path.read_text().splitlines()

def writeInitialList(path: Path, initial_list: list) -> None:
    with path.open("w", encoding="utf-8") as file:
        for value in initial_list:
            file.write(f"{value}\n")

def initializeFile(path: Path, initial_list: list) -> list[str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        writeInitialList(path, initial_list)
    return returnFileValues(path)

def removeValueFromFile(path: Path, value: str) -> None:
    with path.open('r') as file:
        lines = file.readlines()
    with path.open('w') as file:
        for line in lines:
            if line.strip('\n') != value:
                file.write(line)

def resourcePath(relative_path):
    try:
        base_path = Path(sys._MEIPASS)
    except Exception:
        current_path = Path(__file__).parent
        while current_path.name != "DigitalTransmissionsLog":
            current_path = current_path.parent
            if current_path == current_path.parent:
                raise RuntimeError("Could not find project root 'DigitalTransmissionsLog'")
        base_path = current_path

    return base_path / relative_path