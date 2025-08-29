document.addEventListener('DOMContentLoaded', () => {
    const dashboardView = document.getElementById('dashboard-view');
    const uploadView = document.getElementById('upload-view');
    const reportView = document.getElementById('report-view');
    const analyzeNewBtn = document.getElementById('analyze-new-btn');
    const backToDashboardBtn = document.getElementById('back-to-dashboard-btn');
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('file-input');
    const tableBody = document.getElementById('dashboard-table-body');
    const noDocsMessage = document.getElementById('no-docs-message');

    const showView = (view) => {
        dashboardView.classList.add('hidden');
        uploadView.classList.add('hidden');
        reportView.classList.add('hidden');
        view.classList.remove('hidden');
    };

    analyzeNewBtn.addEventListener('click', () => showView(uploadView));
    backToDashboardBtn.addEventListener('click', () => {
        loadDashboard();
        showView(dashboardView);
    });

    dropArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => handleFiles(e.target.files));
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.style.borderColor = '#28a745', false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.style.borderColor = '#007bff', false);
    });
    dropArea.addEventListener('drop', (e) => handleFiles(e.dataTransfer.files), false);

    const preventDefaults = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleFiles = (files) => {
        if (files.length === 0) return;
        const formData = new FormData();
        for (const file of files) {
            formData.append('files', file);
        }

        fetch('/api/analyze-batch', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log('Analysis complete:', data);
            loadDashboard();
            showView(dashboardView);
        })
        .catch(error => {
            console.error('Error uploading files:', error);
            alert('An error occurred during upload.');
        });
    };

    const loadDashboard = async () => {
        try {
            const response = await fetch('/api/documents');
            const documents = await response.json();
            
            tableBody.innerHTML = '';
            if (documents.length > 0) {
                noDocsMessage.classList.add('hidden');
                documents.forEach(doc => {
                    const row = tableBody.insertRow();
                    row.innerHTML = `
                        <td>${doc.name}</td>
                        <td>${new Date(doc.upload_date).toLocaleString()}</td>
                        <td>${doc.status}</td>
                        <td>${doc.principles.join(', ') || 'N/A'}</td>
                        <td><button class="view-report-btn" data-id="${doc.id}">View Report</button></td>
                    `;
                });
            } else {
                noDocsMessage.classList.remove('hidden');
            }
        } catch (error) {
            console.error('Failed to load documents:', error);
            noDocsMessage.textContent = 'Error loading documents.';
            noDocsMessage.classList.remove('hidden');
        }
    };

    // Initial load
    loadDashboard();
});
