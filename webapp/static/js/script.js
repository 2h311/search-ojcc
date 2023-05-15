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
  const data = await get_data_from_api(caseNumbers, caseStatusText);

  const tableRow = document.createElement("tr");
  tableRow.innerHTML = `
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
  `;

  for (const item of data) {
    const table = document.createElement("table");
    const caseNumber = item.userInputtedCaseNumber;
    console.log(caseNumber);
    const caption = document.createElement("caption");
    caption.innerText = caseNumber;
    table.appendChild(caption);
    table.appendChild(tableRow);
    console.log(table);

    const cases = item.cases;
    console.log(cases);
    item.cases.forEach((value, index, array) =>{
      let caseNumber = value["caseNumber"];
      let email = value.email;
      let lostTimeCase = value.lostTimeCase;
      let medicalBenefitsCase = value.medicalBenefitsCase;
      let pdfLink = value.pdfLink;
      let telephone = value.telephone;
      console.log(email);
    });
  }
});
