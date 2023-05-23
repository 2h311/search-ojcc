const searchButton = document.querySelector(".js-search-button");
const caseStatusElement = document.querySelector(".js-case-status");
const tableResultsDiv = document.querySelector(".js-table-results");
const loadingAnimationDiv = document.querySelector(".js-loading-animation");

function getCaseNumbers() {
  const cases = new Array();
  const caseNumbers = document.querySelector(
    "input[class|='js-case-no']"
  ).value;
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
          : `<a href="mailto:${email}">${truncate(email)}</a>`
      }
    </td>
		<td>${medicalBenefitsCase}</td>
		<td>${lostTimeCase}</td>
		<td>
			<a href=${pdfLink}>${truncate(pdfLink, 52)}</a>
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
      table = `<div>No response data for ${userInputtedCaseNumber}</div>`;
    } else {
      table = `<table>
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
    }
    tableResultsDiv.innerHTML += table;
  }
  loadingAnimationDiv.innerHTML = ""; // take out the bouncing ball
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
  // display a bouncing ball
  loadingAnimationDiv.innerHTML = `<img src="static/ball-animation.svg" alt="Loading Animation" class="loading-animation--ball">`;
  const caseStatusText = caseStatusElement.selectedOptions[0].text;
  const data = await getDataFromApi(caseNumbers, caseStatusText); // make request to backend
  putApiDataonDOM(data);
});
