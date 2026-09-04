import csv
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "scripts"))

from audit_omnifall_prefall_eligibility import audit_file  # noqa: E402


def test_audit_counts_views_and_unique_trials(tmp_path: Path) -> None:
    path = tmp_path / "labels.csv"
    rows = [
        ["Subject1Trial1Camera1", 8, 0, 2.5, 1, 1, "demo"],
        ["Subject1Trial1Camera1", 1, 2.5, 4.0, 1, 1, "demo"],
        ["Subject1Trial1Camera2", 8, 0, 2.5, 1, 2, "demo"],
        ["Subject1Trial1Camera2", 1, 2.5, 4.0, 1, 2, "demo"],
        ["Subject2ADLCamera1", 3, 0, 5.0, 2, 1, "demo"],
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "label", "start", "end", "subject", "cam", "dataset"])
        writer.writerows(rows)
    result = audit_file(path)
    assert result["annotated_video_views_with_fall"] == 2
    assert result["estimated_unique_fall_trials"] == 1
    assert result["eligible_video_views"] == {
        "at_least_1s": 2, "at_least_2s": 2, "at_least_3s": 0
    }

