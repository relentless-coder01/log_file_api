const form = document.getElementById('log-form');
const logText = document.getElementById('log-text');
const logContainer = document.getElementById('log-container');
const pagination = document.getElementById('pagination');

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const filename = document.getElementById('filename').value;
    const n = document.getElementById('n').value;
    const keyword = document.getElementById('keyword').value;

    await fetchLogs(filename, n, keyword, 1);
});

async function fetchLogs(filename, n, keyword, page) {
    const params = new URLSearchParams({ filename });
    if (n) params.append('n', n);
    if (keyword) params.append('keyword', keyword);
    if (page) params.append('page', page);
    const response = await fetch(`/api/v1/logs?${params.toString()}`);
    const resp = await response.json();

    displayLogs(resp.data);
    if (resp.data.length > 0) {
        setupPagination(resp.page, resp.next_page, resp.previous_page, filename, n, keyword, resp.line_count);
    } else {
        logText.innerHTML = '';
    }
}

function displayLogs(lines) {
    logContainer.innerHTML = lines.map(line => `<div class="log-line">${line}</div>`).join('');
}

function setupPagination(currentPage, next_page, previous_page, filename, n, keyword, lineCount) {
    pagination.innerHTML = '';
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

    if (next_page != null) {
        let nextButton = document.createElement('button');
        nextButton.innerHTML = 'next';
        nextButton.className = "next-page-btn";
        nextButton.onclick = () => fetchLogs(filename, n, keyword, currentPage + 1);
        document.getElementById('pagination').appendChild(nextButton);
    }
}