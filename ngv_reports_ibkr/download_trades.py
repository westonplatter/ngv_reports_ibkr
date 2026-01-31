import time

from loguru import logger

from ngv_reports_ibkr.adapters import ReportOutputAdapterCSV
from ngv_reports_ibkr.config_helpers import get_config, get_ib_json
from ngv_reports_ibkr.custom_flex_report import CustomFlexReport


def fetch_report(
    flex_token: int, query_id: int, cache_report_on_disk: bool = False
) -> CustomFlexReport:
    """
    Fetch report. Optionally save to disk (helpful for debugging)

    Args:
        flex_token (int): IB Flex Token
        query_id (int): IB Report Query Id
        cache_report_on_disk (bool, optional): Cache XML content on disk. Helpful for debugging. Defaults to False.

    Returns:
        CustomFlexReport: [description]
    """
    report = CustomFlexReport(token=flex_token, queryId=query_id)

    # save report
    if cache_report_on_disk:
        epoch_time = int(time.time())
        report_path = f"data/flex_report_{epoch_time}.xml"
        logger.debug(f"save file to disk {report_path}")
        report.save(report_path)

    return report


def load_report(xml_file_path: str) -> CustomFlexReport:
    """
    Load CustomFlexReport from provided file path

    Args:
        xml_file_path (str): file path to the cached XML file

    Returns:
        CustomFlexReport: report
    """
    report = CustomFlexReport()
    report.load(xml_file_path)
    return report


def execute_csv_for_accounts(
    report_name: str, cache: bool = False, file_name: str = ".env"
):
    """
    Execute the trades dowload process for accounts

    Args:
        report_name (str): report name as it exists in the env file. Eg, report_name=xyz, in env file=IB_REPORT_ID_XYZ
        cache (bool): cache XML
        file_name (str): env file name. Defaults to ".env".

    """
    configs = get_config(file_name)
    data = get_ib_json(configs)

    if "accounts" not in data:
        return None

    for account in data["accounts"]:
        query_id = int(account[report_name.lower()])
        if query_id <= 0:
            logger.warning(f"{account['name']} does not have a {report_name} query_id")
            continue
        flex_token = account["flex_token"]
        report = fetch_report(flex_token, query_id, cache_report_on_disk=cache)
        output_adapter = ReportOutputAdapterCSV(data_folder="data", report=report)
        output_adapter.process_accounts()
