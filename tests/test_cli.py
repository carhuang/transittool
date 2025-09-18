import sys
from pathlib import Path
import csv


def read_journey_ids(path):
    jids = set()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # be tolerant of casing/spelling differences
            if "JourneyId" in r and r["JourneyId"] is not None and r["JourneyId"].strip() != "":
                jids.add(r["JourneyId"].strip())
            else:
                # fallback: try to pick a column that looks like a journey id
                for v in r.values():
                    if v and v.startswith("TESTJID_") or (v and "T" in v and ":" in v):
                        jids.add(v.strip())
    return jids


def test_data_dir_and_get_data_path(transittool_module, tmp_path):
    mod = transittool_module
    expected_data_dir = Path(tmp_path) / ".local" / "share" / "transittool"
    assert mod.DATA_DIR == expected_data_dir
    assert expected_data_dir.exists()
    gp = mod.get_data_path("master.csv")
    assert gp == expected_data_dir / "master.csv"


def test_init_creates_master_meta_index(transittool_module, sample_csv_path):
    mod = transittool_module
    raw = sample_csv_path

    old_argv = sys.argv.copy()
    sys.argv[:] = ["transittool", "init", str(raw)]
    try:
        mod.main()
    finally:
        sys.argv[:] = old_argv

    master = mod.get_data_path("master.csv")
    meta = mod.get_data_path("master.csv" + mod.META_SUFFIX)
    index = mod.get_data_path("master.csv" + mod.INDEX_SUFFIX)

    assert master.exists(), "master.csv should be created by init"
    assert meta.exists(), "meta file should be created by init"
    assert index.exists(), "index file should be created by init"


def test_append_adds_new_journeys(transittool_module, tmp_path, sample_csv_path):
    mod = transittool_module
    # Initialize using the sample CSV
    old_argv = sys.argv.copy()
    sys.argv[:] = ["transittool", "init", str(sample_csv_path)]
    try:
        mod.main()
    finally:
        sys.argv[:] = old_argv

    master = mod.get_data_path("master.csv")
    before_jids = read_journey_ids(master)

    # Create a small raw file with two guaranteed-new journey ids
    raw2 = tmp_path / "raw_new.csv"
    headers = ["DateTime", "Transaction", "Product", "Amount", "BalanceDetails", "JourneyId", "LocationDisplay", "TransactonTime"]
    rows = [
        ["Jul-01-2025 09:00", "Purchase", "StoredValue", "$1.00", "", "TESTJID_NEW1", "Station X", "09:00"],
        ["Jul-02-2025 10:00", "Purchase", "StoredValue", "$2.00", "", "TESTJID_NEW2", "Station Y", "10:00"],
    ]
    raw2.parent.mkdir(parents=True, exist_ok=True)
    with open(raw2, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in rows:
            writer.writerow(r)

    sys.argv[:] = ["transittool", "append", str(raw2)]
    try:
        mod.main()
    finally:
        sys.argv[:] = old_argv

    after_jids = read_journey_ids(master)
    # Expect at least two new journey ids added
    assert len(after_jids) >= len(before_jids) + 2


def test_summary_and_date_cli_outputs(transittool_module, sample_csv_path, capsys):
    mod = transittool_module
    # Ensure master exists by initializing with sample CSV
    old_argv = sys.argv.copy()
    sys.argv[:] = ["transittool", "init", str(sample_csv_path)]
    try:
        mod.main()
    finally:
        sys.argv[:] = old_argv

    # date command
    sys.argv[:] = ["transittool", "date"]
    try:
        mod.main()
    finally:
        sys.argv[:] = old_argv
    captured = capsys.readouterr()
    assert captured.out.strip() != "", "date command should print a date range"

    # summary command
    sys.argv[:] = ["transittool", "summary"]
    try:
        mod.main()
    finally:
        sys.argv[:] = old_argv
    captured = capsys.readouterr()
    assert captured.out.strip() != "", "summary command should print something readable"