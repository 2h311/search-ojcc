import re

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag


search_text = "response to petition for benefits filed by"
ojcc_case_no = "17-000001"


def get_jcc_html(ojcc_case_no: str):
    request_url = "https://www.jcc.state.fl.us/JCC/searchJCC/searchAction.asp?sT=byCase"
    response = requests.post(
        request_url, data={"caseNum": ojcc_case_no, "Search": "+Search+"}
    )
    response.raise_for_status()
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
            pdf_link = f'{"https://www.jcc.state.fl.us"}{pdf_table_data.find("a").get("href")}'
            pdf_link_list.add(pdf_link)

    if pdf_link_list:
        print(pdf_link_list)
    else:
        print("No case records found ...")


div_docket = get_jcc_html(ojcc_case_no)
if div_docket:
	pdfs = get_pdf_links(div_docket)