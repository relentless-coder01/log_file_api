const form = document.getElementById('log-form');
const logText = document.getElementById('log-text');
const logContainer = document.getElementById('log-container');
const pagination = document.getElementById('pagination');
const pageNum = document.getElementById('page-num');
const pageLinks = document.getElementById('page-links');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const filename = document.getElementById('filename').value;
    const n = document.getElementById('n').value;
    const keyword = document.getElementById('keyword').value;

    await fetchLogs(filename, n, keyword, 1);

});

function showSpinner() {
    document.getElementById('spinner').style.display = "block";
    document.getElementById('page-content').classList.add("fadeOut");
}

function hideSpinner() {
    document.getElementById('spinner').style.display = "none";
    document.getElementById('page-content').classList.remove("fadeOut");
}

function clearLogContainer() {
    logContainer.innerHTML = '';
    pageNum.innerHTML = '';
    pagination.innerHTML = '';
}

async function fetchLogs(filename, n, keyword, page) {
    showSpinner()
    const params = new URLSearchParams({ filename });
    if (n) params.append('n', n);
    if (keyword) params.append('keyword', keyword);
    if (page) params.append('page', page);
    const response = await fetch(`/api/v1/logs?${params.toString()}`);
    const resp = await response.json();
    if (response.status == 200) {
        displayLogs(resp.data);
        if (resp.data.length > 0) {
            setupPagination(resp.page, resp.next_page, resp.previous_page, filename, n, keyword, resp.line_count);
        } else {
            clearLogContainer();
        }
    } else if (response.status == 404) {
        alert(resp.message)
        clearLogContainer();
    } else {
        alert("Internal server error. Please try again later.")
        clearLogContainer();
    }
    hideSpinner()
}

function displayLogs(lines) {
    logContainer.innerHTML = lines.map(line => `<div class="log-line">${line}</div>`).join('');
}

function setupPagination(currentPage, next_page, previous_page, filename, n, keyword, lineCount) {
    pagination.innerHTML = '';
    pageLinks.innerHTML = '';
    prev = currentPage - 1;
    next = currentPage + 1;
    document.getElementById('page-num').innerHTML = 'Page ' + currentPage + '(Lines: ' + lineCount + ')';
    if (previous_page != null) {
        let prevButton = document.createElement('button');
        prevButton.innerHTML = 'prev';
        prevButton.className = "prev-page-btn";
        prevButton.onclick = () => fetchLogs(filename, n, keyword, currentPage - 1);
        document.getElementById('pagination').appendChild(prevButton);
    }
//    let pageLinkDiv = document.createElement('div');
//    pageLinkDiv.className = "page-link-div";
//    document.getElementById('pagination').appendChild(pageLinkDiv);
    // Create Pagination numbers
    for(let i = 1; i <= currentPage; i++) {
        let pageLink = document.createElement("a");
        pageLink.textContent = i;
        pageLink.setAttribute("href", "#");
        pageLink.onclick = () => fetchLogs(filename, n, keyword, i);
        if(i == currentPage) {
            pageLink.className = "page-link active-page";
        } else {
            pageLink.className = "page-link";
        }
        pageLinks.appendChild(pageLink);
    }
    if (next_page != null) {
        let nextButton = document.createElement('button');
        nextButton.innerHTML = 'next';
        nextButton.className = "next-page-btn";
        nextButton.onclick = () => fetchLogs(filename, n, keyword, currentPage + 1);
        document.getElementById('pagination').appendChild(nextButton);
    }
}