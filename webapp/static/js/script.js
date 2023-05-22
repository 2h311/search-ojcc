const searchButton = document.querySelector(".js-search-button");
const caseStatusElement = document.querySelector(".js-case-status");
const tableResultsDiv = document.querySelector(".js-table-results");

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

function getTableBody(cases) {
  let tbodyElement = "<tbody>";
  cases.forEach((value, index, array) => {
    tbodyElement += `
      <tr>
        <td>${value.caseNumber}</td>
        <td>${value.telephone}</td>
        <td>${value.email}</td>
        <td>${value.medicalBenefitsCase}</td>
        <td>${value.lostTimeCase}</td>
        <td>
          <a href=${value.pdfLink}>${value.pdfLink}</a>
        </td>
      </tr>
    `;
  });
  tbodyElement += "</tbody>";
  return tbodyElement;
}

async function getDataFromApi(caseNumbers, caseStatusText) {
  const response = await fetch("/api", {
    method: "POST",
    headers: { Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify({
      caseStatus: caseStatusText,
      caseNumbers: caseNumbers,
    }),
  });
  return await response.json();
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
  // TODO: display a loading spinner

  // make request to backend
  const data = await getDataFromApi(caseNumbers, caseStatusText);

  for (const item of data) {
    const { userInputtedCaseNumber, cases } = item;
    let table = `<table>
      <caption>${userInputtedCaseNumber}</caption>
      <thead>
        <tr>
          <th>Case &num;</th>
          <th>Telephone</th>
          <th>Email</th>
          <th>Medical Benefits Case</th>
          <th>Lost Time Case</th>
          <th>PDF Link</th>
        </tr>
      </thead>
      ${getTableBody(cases)}
    </table>`;
    tableResultsDiv.innerHTML = table;
  }
});
