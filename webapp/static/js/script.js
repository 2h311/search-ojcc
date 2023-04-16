const searchButton = document.querySelector(".js-search-button");
const caseStatusElement = document.querySelector(".js-case-status");

function getCaseNumbers() {
  const caseNumbers = new Array();
  document
    .querySelectorAll("input[class|='js-case-no']")
    .forEach((pageElement) => {
      if (pageElement.value !== "") {
        caseNumbers.push(pageElement.value);
        pageElement.value = "";
      }
    });
  return caseNumbers;
}

async function get_data_from_api(caseNumbers, caseStatusText) {
  const response = await fetch("/api", {
    method: "POST",
    headers: { Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify({
      caseStatus: caseStatusText,
      caseNumbers: caseNumbers,
    }),
  });
  // TODO: display a loading spinner
  json = await response.json();
  console.log(json);
}

searchButton.addEventListener("click", async function () {
  if (caseStatusElement.selectedOptions[0].text === "CASE STATUS") {
    console.log("You need to select a case status from the dropdown");
  }

  const caseNumbers = getCaseNumbers();
  if (!caseNumbers.length) {
    console.log("You need to enter one or two case numbers...");
    return;
  }

  let caseStatusText = caseStatusElement.selectedOptions[0].text;
  // make request to backend
  await get_data_from_api(caseNumbers, caseStatusText);
});
