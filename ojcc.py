import re
import io
import logging

import requests
from bs4.element import Tag
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_pages


# disable request logging messages
logging.getLogger("requests").disabled = True
logging.getLogger("urllib3").disabled = True


logging.basicConfig(format="%(message)s")
logger = logging.getLogger("ojcc")
logger.setLevel(logging.DEBUG)


search_text = "response to petition for benefits filed by"
ojcc_case_no = "17-000006"


def get_jcc_html(ojcc_case_no: str) -> Tag:
    request_url = "https://www.jcc.state.fl.us/JCC/searchJCC/searchAction.asp?sT=byCase"
    logger.debug(f"Visiting url -> {request_url}")
    response = requests.post(
        request_url, data={"caseNum": ojcc_case_no, "Search": "+Search+"}, timeout=45
    )
    response.raise_for_status()
    logger.debug("Response OK. Cooking a beautiful soup")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.select_one("div#docket")


def get_pdf_links(div_docket: Tag, pdf_links: set = set()) -> set:
    html_table_rows = div_docket.select("tr")

    # skip the first html table row
    for html_table in html_table_rows[1:]:
        pdf_table_data, date_table_data, proceedings_table_data = html_table.select(
            "td"
        )
        if proceedings_table_data.text.lower().__contains__(
            search_text
        ) and pdf_table_data.find("a"):
            pdf_links.add(f'{pdf_table_data.find("a").get("href")}')

    logger.debug(f"Found {len(pdf_links) or 0} case records")
    return pdf_links


div_docket = get_jcc_html(ojcc_case_no)
if div_docket:
    pdf_links = get_pdf_links(div_docket)


pdf_link = pdf_links.pop()

request_url = f"https://www.jcc.state.fl.us{pdf_link}"
logger.debug(f"Downloading pdf -> {pdf_link}")
# download pdf
response = requests.get(request_url, stream=True)
response.raise_for_status()
logger.debug("Download Successful. Reading content of PDF file")

text = extract_text(io.BytesIO(response.content))
case_number = re.search("OJCC Case No.: (\S+)", text).groups()[0]
logger.info(f"Case Number: {case_number}")

telephone = re.search("\d{3}-\d{3}-\d{4}", text).group()
logger.info(f"Telephone: {telephone}")

email = re.search(
    "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", text
).group()
logger.info(f"Email: {email}")

medical_benefits_case = re.search("MEDICAL BENEFITS CASE:\s+(\S+)", text).groups()[0]
logger.info(f"MEDICAL BENEFITS CASE: {medical_benefits_case}")

re.search("LOST TIME CASE:\s*", text)
