from pathlib import Path

from src.pim_asset_inspector.asset_inspector import (
    inspect_assets,
    write_required_asset_report,
)
from src.pim_asset_inspector.config_loader import load_rules_from_json
from src.pim_asset_inspector.report_writer import (
    build_report_rows,
    write_csv_report,
)


def main() -> None:
    asset_folder = Path("data/sample/pim_assets")
    rules_path = Path("config/pim_asset_rules.json")
    file_report_path = Path("docs/examples/pim_asset_file_report.csv")
    required_asset_report_path = Path("docs/examples/required_asset_report.csv")

    rules = load_rules_from_json(rules_path)

    inspection_results = inspect_assets(
        asset_folder,
        rules,
    )

    file_report_rows = build_report_rows(
        inspection_results,
    )

    write_csv_report(
        file_report_rows,
        file_report_path,
    )

    required_views = ["FRONT", "BACK", "SIDE"]

    write_required_asset_report(
        inspection_results,
        required_views,
        required_asset_report_path,
    )


if __name__ == "__main__":
    main()