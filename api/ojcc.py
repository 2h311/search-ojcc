import functools
import io
import logging
import re
from typing import Callable

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag as BeautifulSoupTag
from models import DataToBeReturned
from models import OjccCaseData
from pdfminer.high_level import extract_text


logging.basicConfig(format="... %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
proceedings_search_text = "response to petition for benefits filed by"
email_regex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.(\s)*[A-Z|a-z]{2,})+"


def retry_wraps(times: int = 3) -> Callable:
    def retry(function) -> Callable:
        """tries to run a function after an unsuccessful attempt."""

        @functools.wraps(function)
        def inner(*args, **kwargs):
            for _ in range(times):
                try:
                    return function(*args, **kwargs)
                except Exception as err:
                    logger.error(err)

        return inner

    return retry


@retry_wraps()
def get_jcc_html(ojcc_case_no: str) -> BeautifulSoupTag:
    request_url = "https://www.jcc.state.fl.us/JCC/searchJCC/searchAction.asp?sT=byCase"
    logger.debug(f"Searching ojcc case number {ojcc_case_no} at {request_url}")
    response = requests.post(
        request_url, data={"caseNum": ojcc_case_no, "Search": "+Search+"}, timeout=45
    )
    response.raise_for_status()
    logger.debug("Server Response OK. Cooking a beautiful soup")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.select_one("div#docket")


def get_pdf_links(div_docket: BeautifulSoupTag, pdf_links: set[str] = set()) -> set:
    html_table_rows = div_docket.select("tr")

    # skip the first html table row
    for html_table in html_table_rows[1:]:
        pdf_table_data, date_table_data, proceedings_table_data = html_table.select(
            "td"
        )
        if proceedings_table_data.text.lower().__contains__(
            proceedings_search_text
        ) and pdf_table_data.find("a"):
            pdf_links.add(f'{pdf_table_data.find("a").get("href")}')

    logger.debug(f"Found {len(pdf_links) or 0} case records")
    return pdf_links


def parse_and_extract_pdf_file(data_dict: dict[str], text: str) -> None:
    case_number = re.search(r"OJCC Case No.: (\S+)", text).groups()[0]
    logger.info(f"Case Number: {case_number}")
    data_dict["caseNumber"] = case_number

    telephone = re.search(r"\d{3}-\d{3}-\d{4}", text).group()
    logger.info(f"Telephone: {telephone}")
    data_dict["telephone"] = telephone

    email = re.search(email_regex, text, re.M | re.I).group()
    email = re.sub(
        "\\s", "", email.lower()
    )  # remove any whitespace contained in the email, if any
    logger.info(f"Email: {email}")
    data_dict["email"] = email

    medical_benefits_case = re.search(r"MEDICAL BENEFITS CASE:\s+(\S+)", text)
    medical_benefits_case = medical_benefits_case.groups()[0]
    logger.info(f"Medical Benefits Case: {medical_benefits_case}")
    data_dict["medicalBenefitsCase"] = medical_benefits_case

    lost_time_case = re.search(r"LOST TIME CASE:\s+(No|Yes)", text).groups()[0]
    logger.info(f"Lost Time Case: {lost_time_case}")
    data_dict["lostTimeCase"] = lost_time_case
    print()


@retry_wraps()
def get_pdf_content(pdf_link: str) -> bytes:
    request_url = f"https://www.jcc.state.fl.us{pdf_link}"
    logger.debug(f"Downloading pdf from {pdf_link}")
    # download pdf
    response = requests.get(request_url, stream=True, timeout=45)
    response.raise_for_status()
    logger.debug("Download Successful. Reading and Parsing content of .pdf file")
    return response.content


def get_all_data_from_case_no(ojcc_case_no: str) -> list[OjccCaseData | None]:
    all_data_list = list()
    div_docket = get_jcc_html(ojcc_case_no)

    if div_docket:
        pdf_links = get_pdf_links(div_docket)
        while pdf_links:
            data_dict = dict()
            pdf_link = pdf_links.pop()
            data_dict["pdfLink"] = pdf_link
            pdf_content_in_bytes = get_pdf_content(pdf_link)
            text = extract_text(io.BytesIO(pdf_content_in_bytes))
            parse_and_extract_pdf_file(data_dict, text)
            all_data_list.append(data_dict)

    if not all_data_list:
        logger.error(
            f"Can't find any case file in the ojcc case number you've provided {ojcc_case_no}"
        )
    return all_data_list


def get_data_for_multiple_case_numbers(
    case_number_list: list,
) -> DataToBeReturned | None:
    for string in case_number_list:
        pipeline = dict()
        returned_data = get_all_data_from_case_no(string)
        pipeline["userInputtedCaseNumber"] = string
        if returned_data:
            pipeline["cases"] = returned_data
        yield pipeline
    # TODO: add a flag that will signify to the FE to stop probing...


if __name__ == "__main__":
    for r in get_data_for_multiple_case_numbers(
        [
            "17-00022",
            "17-00012",
        ]
    ):
        print(r)
