const searchButton = document.querySelector(".js-search-button");
const caseStatusElement = document.querySelector(".js-case-status");
const tableResultsDiv = document.querySelector(".js-table-results");
const loadingAnimationDiv = document.querySelector(".js-loading-animation");
const caseInputElement = document.querySelector(".js-case-no-1");

function getCaseNumbers() {
  const cases = new Array();
  const caseNumbers = caseInputElement.value;
  caseNumbers.split(",").forEach((string) => {
    if (string.length) {
      cases.push(string.trim());
    }
  });
  return cases;
}

function getTableBody(cases) {
  let tbodyElement = "<tbody>";
  cases.forEach((value, index, array) => {
    const {
      caseNumber,
      telephone,
      email,
      medicalBenefitsCase,
      lostTimeCase,
      pdfLink,
    } = value;
    tbodyElement += `
	  <tr>
		<td>${caseNumber}</td>
		<td>${telephone}</td>
		<td>
      ${
        email === "Not Found"
          ? "<span>Not Found</span>"
          : `<a href="mailto:${email}">${truncate(email, 20)}</a>`
      }
    </td>
		<td>${medicalBenefitsCase}</td>
		<td>${lostTimeCase}</td>
		<td>
			<a href=${pdfLink} target='_blank'>${truncate(pdfLink, 30)}</a>
		</td>
	  </tr>
	`;
  });
  tbodyElement += "</tbody>";
  return tbodyElement;
}

function putApiDataonDOM(data) {
  for (const item of data) {
    const { userInputtedCaseNumber, cases } = item;
    let table;
    if (!cases.length) {
      table = `<div>Can&apos;t Find No Case Data For ${userInputtedCaseNumber}</div>`;
    } else {
      table = `<table>
		  <caption>${userInputtedCaseNumber}</caption>
		  <thead>
			<tr>
			  <th>Case &num;</th>
			  <th>Telephone</th>
			  <th>Email</th>
			  <th>Medical<br>Benefits</th>
			  <th>Lost<br>Time</th>
			  <th>PDF<br>Link</th>
			</tr>
		  </thead>
		  ${getTableBody(cases)}
	  </table>`;
    }
    tableResultsDiv.innerHTML += table;
  }
  loadingAnimationDiv.innerHTML = ""; // take out the bouncing ball when we done processing response from the backend
  caseInputElement.value = ""; // clear the input
}

async function getDataFromApi(caseNumbers, caseStatusText) {
  const response = await fetch("/api/", {
    method: "POST",
    headers: { Accept: "application/json", "Content-Type": "application/json" },
    body: JSON.stringify({
      caseStatus: caseStatusText,
      caseNumbers: caseNumbers,
    }),
  });
  return await response.json();
}

function truncate(string, number = 32) {
  let response = string;
  if (string.length > number) {
    response = string.slice(0, number - 1) + "&hellip;";
  }
  return response;
}

searchButton.addEventListener("click", async function () {
  const caseNumbers = getCaseNumbers();
  if (!caseNumbers.length) {
    // TODO: display a red alert asking them to input something
    return;
  }

  tableResultsDiv.innerHTML = ""; // clear any existing table if any
  // display bouncing ball animation
  loadingAnimationDiv.innerHTML = `
    <div class="loadingio-spinner-ball-oha5k74jaw7">
      <div class="ldio-jxs6a0c8pv">
        <div></div>
      </div>
    </div>`;
  const data = await getDataFromApi(
    caseNumbers,
    caseStatusElement.selectedOptions[0].text
  ); // make request to backend
  putApiDataonDOM(data);
});
