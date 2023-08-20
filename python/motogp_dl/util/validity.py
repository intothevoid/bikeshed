# Description: This file contains functions that check the validity of a download type
import re
import yaml
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_dl_type_score(title: str, filters: dict) -> int:
    # Initialize score
    score = 0

    # Get positive and negative filters
    POSITIVE_FILTERS = filters["POSITIVE_FILTERS"]
    NEGATIVE_FILTERS = filters["NEGATIVE_FILTERS"]

    # Check for matches with positive filters
    for filter in POSITIVE_FILTERS:
        if re.search(filter, title):
            score += 1

    # Check for matches with negative filters
    for filter in NEGATIVE_FILTERS:
        if re.search(filter, title):
            return 0

    return score


def check_valid_dl_type(title: str, settings: dict) -> bool:
    if get_dl_type_score(title, settings) > 0:
        return True
    else:
        return False


def test_check_valid_dl_type():
    """Test check_valid_dl_type()"""

    # read config.yml file
    with open(f"{get_project_root()}/config.yaml", "r") as f:
        SETTINGS = yaml.safe_load(f)

    # Create list of titles
    titles = [
        "MotoGP.Sprint.Race",
        "MotoGP.2023x10.Austria",
        "MotoGP.2023x10.Austria.1080p",
        "MotoGP.2023x10.Austria.FP2.1080p.Eng",
        "Moto2.2023x10.Austria.Practice.Three.1080p",
        "Qualifying.MotoGP",
        "Qualifying.Moto3" "Qualifying.Moto2",
        "MotoGP.Sprint.Race",
        "MotoGP.2023x10.Austria.Practice.1080p.Eng",
        "MotoGP.2023x10.Austria.FP1.1080p.Eng",
        "MotoGP.2023x10.Austria.FP2 - French",
        "MotoGP.2023x10.Austria.Q1 Q2 - French",
        "Moto2.2023x10.Austria.Practice.One",
        "Moto2.2023x10.Austria.Practice.Two",
        "Moto3.2023x10.Austria.Practice.One",
        "Moto3.2023x10.Austria.Practice.Two",
        "MotoGP.2023x10.Austria.PC.Part1",
        "MotoGP.2023x10.Austria.PC.Part2",
        "NASCAR Xfinity Series 2023. R23. Shriners Children's 200 at The Glen. Weekend On NBC",
        "MotoGP Red Bull Ring Qualifying - MotoGP 2023",
        "ARCA.Menards.Series.2023x13.General.Tire.100.at.The.Glen",
        "MotoGP.2023x10.Austria.Q1-Q2",
        "MotoGP.2023x10.Austria.FP2",
        "[Request] sprint race Austria",
        "ANNOUNCEMENT: New posting rule",
        "ANNOUNCEMENT: Some file hosting sites blocked by Reddit",
        "MotoGP.2023x10.Austria",
        "NASCAR Xfinity Series 2023. R23. Shriners Children's 200 at The Glen. Weekend On NBC",
        "[Request] sprint race Austria",
        "MotoGP Red Bull Ring Austria SPRINT - MotoGP 2023",
        "MotoGP Red Bull Ring Qualifying - MotoGP 2023",
        "Something weird has happened to our MotoGP 'distribution system', hasn't it?",
        "[REQUEST] MotoGP Qualifying in English. Austria",
        "NASCAR.Xfinity.Series.2023x23.Shriners.Children's.200.at.The.Glen",
        "DTM Lausitzring Race 1",
        "2023 Supercars Championship Round 8 Tailem Bend",
        "Race 1 | Road America | Fanatec GT World Challenge America Powered by AWS 2023",
        "[request] moto E race Austria",
        "DTM 2023 R05 Lausitzring - Race 1",
        "ARCA.Menards.Series.2023x13.General.Tire.100.at.The.Glen",
        "MotoGP.2023x10.Austria.Q1-Q2",
        "Race 1 | Okayama | Fanatec GT World Challenge Asia 2023",
        "[Request] Super Formula: Motegi",
        "MotoGP.2023x10.Austria.FP2",
        "ARCA Menards Series 2023. R13. General Tire 100 at The Glen. FS1. 720P",
        "[Request] Beyond All Limits Season 2 form F1TV",
        "[Request] Supercars - Round 7 Sydney",
        "Request - MotoGP practise",
        "2016 Abu Dhabi Post Race Press Conference",
        "2023 IMSA SportsCar Championship (Round 8) Road America",
        "BTCC 2023 - Round 7 - Knockhill",
    ]

    # Iterate over titles and check if they are valid
    for title in titles:
        valid = check_valid_dl_type(title, SETTINGS)
        print(f"{title}: {valid}")


if __name__ == "__main__":
    test_check_valid_dl_type()
