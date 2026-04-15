document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('queryInput');
    const btn = document.getElementById('searchBtn');
    const loading = document.getElementById('loading');
    const resultsArea = document.getElementById('resultsArea');
    const errorArea = document.getElementById('errorArea');
    const sqlOutput = document.getElementById('sqlOutput');
    const tableHead = document.getElementById('tableHead');
    const tableBody = document.getElementById('tableBody');
    const rowCount = document.getElementById('rowCount');

    const executeQuery = async () => {
        const queryText = input.value.trim();
        if (!queryText) return;

        // UI Reset
        resultsArea.classList.add('hidden');
        errorArea.classList.add('hidden');
        loading.classList.remove('hidden');

        try {
            const resp = await fetch('http://127.0.0.1:8000/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: queryText })
            });

            if (!resp.ok) {
                throw new Error('Failed to fetch data from API');
            }

            const data = await resp.json();
            
            // Populate SQL
            sqlOutput.textContent = data.sql;

            // Populate Table
            tableHead.innerHTML = '';
            tableBody.innerHTML = '';
            
            if (data.columns && data.columns.length > 0) {
                const trHead = document.createElement('tr');
                data.columns.forEach(col => {
                    const th = document.createElement('th');
                    th.textContent = col;
                    trHead.appendChild(th);
                });
                tableHead.appendChild(trHead);
            }

            if (data.rows && data.rows.length > 0) {
                data.rows.forEach(row => {
                    const trBody = document.createElement('tr');
                    row.forEach(val => {
                        const td = document.createElement('td');
                        td.textContent = (val === null || val === undefined) ? 'NULL' : val;
                        trBody.appendChild(td);
                    });
                    tableBody.appendChild(trBody);
                });
                rowCount.textContent = `${data.rows.length} rows`;
            } else {
                const trBody = document.createElement('tr');
                const td = document.createElement('td');
                td.colSpan = data.columns ? data.columns.length : 1;
                td.textContent = 'No results found.';
                td.style.textAlign = 'center';
                td.style.color = 'var(--text-muted)';
                trBody.appendChild(td);
                tableBody.appendChild(trBody);
                rowCount.textContent = `0 rows`;
            }

            resultsArea.classList.remove('hidden');
        } catch (err) {
            document.getElementById('errorMsg').textContent = err.message || 'An error occurred';
            errorArea.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
        }
    };

    btn.addEventListener('click', executeQuery);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') executeQuery();
    });
});
