import re
import logging

import requests
from bs4.element import Tag
from bs4 import BeautifulSoup


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


def get_pdf_links(div_docket: Tag) -> set:
    pdf_link_list = set()
    html_table_rows = div_docket.select("tr")

    # skip the first html table row
    for html_table in html_table_rows[1:]:
        pdf_table_data, date_table_data, proceedings_table_data = html_table.select(
            "td"
        )
        if proceedings_table_data.text.lower().__contains__(
            search_text
        ) and pdf_table_data.find("a"):
            pdf_link = (
                f'{"https://www.jcc.state.fl.us"}{pdf_table_data.find("a").get("href")}'
            )
            pdf_link_list.add(pdf_link)

    if pdf_link_list:
        print(pdf_link_list)
    else:
        print("No case records found ...")


div_docket = get_jcc_html(ojcc_case_no)
if div_docket:
    reuslt = get_pdf_links(div_docket)
