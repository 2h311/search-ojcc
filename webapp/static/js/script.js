const searchButton = document.querySelector(".js-search-button");
const caseStatusElement = document.querySelector(".js-case-status");

function getCaseNumbers() {
  const caseNumbers = new Array();
  document
    .querySelectorAll("input[class|='js-case-no']")
    .forEach((pageElement) => {
      if (pageElement.value !== "") {
        caseNumbers.push(pageElement.value);
      }
    });
  return caseNumbers;
}

async function get_data_from_api(request_payload) {
  console.log(request_payload);
}

searchButton.addEventListener("click", function (event) {
  if (caseStatusElement.selectedOptions[0].text === "CASE STATUS") {
    console.log("You need to select a case status from the dropdown");
  }

  const caseNumbers = getCaseNumbers();
  if (caseNumbers.length) {
    let caseStatusText = caseStatusElement.selectedOptions[0].text;
    console.log("Case Status: ", caseStatusText);
    console.log("caseNumbers: ", caseNumbers);
    // make request to backend
    get_data_from_api();
  }
});
