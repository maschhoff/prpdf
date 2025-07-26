import os
import logging

STATUS_FILE = "/tmp/update_flag.txt"

# Logger konfigurieren (ggf. an dein Logging-Setup anpassen)
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

def _ensure_file_exists():
    if not os.path.isfile(STATUS_FILE):
        try:
            with open(STATUS_FILE, "w") as f:
                f.write("0")  # Default: kein Update nötig
            logger.info(f"Status-Datei angelegt: {STATUS_FILE}")
        except Exception as e:
            logger.error(f"Fehler beim Anlegen der Status-Datei {STATUS_FILE}: {e}")

def set_update_needed(value: bool):
    _ensure_file_exists()
    try:
        with open(STATUS_FILE, "w") as f:
            f.write("1" if value else "0")
        logger.info(f"Update-Flag gesetzt auf {'1' if value else '0'} in {STATUS_FILE}")
    except Exception as e:
        logger.error(f"Fehler beim Schreiben in die Status-Datei {STATUS_FILE}: {e}")

def get_update_needed() -> bool:
    _ensure_file_exists()
    try:
        with open(STATUS_FILE, "r") as f:
            val = f.read(1)
        result = val == "1"
        logger.debug(f"Update-Flag aus {STATUS_FILE} gelesen: {val}")
        return result
    except Exception as e:
        logger.error(f"Fehler beim Lesen der Status-Datei {STATUS_FILE}: {e}")
        return False
