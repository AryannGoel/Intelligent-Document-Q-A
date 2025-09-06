// static/script.js

document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const qaForm = document.getElementById('qa-form');
    const uploadStatus = document.getElementById('upload-status');
    const qaSection = document.getElementById('qa-section');
    const chatMessages = document.getElementById('chat-messages');
    const questionInput = document.getElementById('question-input');
    const filenameDisplay = document.getElementById('filename-display');
    const fileInput = document.getElementById('document-input');
    const urlInput = document.getElementById('url-input');
    
    let currentFilename = '';

    // Handle Source Submission (File or URL)
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = fileInput.files[0];
        const url = urlInput.value.trim();

        if (!file && !url) {
            uploadStatus.textContent = 'Error: Please select a file or enter a URL.';
            uploadStatus.style.color = 'red';
            return;
        }

        const formData = new FormData();
        if (file) {
            formData.append('document', file);
        } else if (url) {
            formData.append('url', url);
        }

        uploadStatus.textContent = 'Processing source... This may take a moment.';
        uploadStatus.style.color = '#333';
        
        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();

            if (response.ok) {
                uploadStatus.textContent = result.message;
                uploadStatus.style.color = 'green';
                currentFilename = result.filename;
                filenameDisplay.textContent = currentFilename;
                qaSection.classList.remove('hidden');
            } else {
                throw new Error(result.error || 'Unknown error occurred.');
            }
        } catch (error) {
            uploadStatus.textContent = `Error: ${error.message}`;
            uploadStatus.style.color = 'red';
        }
    });

    // Handle Question Answering
    qaForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = questionInput.value.trim();
        if (!question || !currentFilename) return;

        appendMessage(question, 'user');
        questionInput.value = '';

        const loadingIndicator = appendMessage('Thinking...', 'ai');
        
        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question, filename: currentFilename }),
            });
            
            chatMessages.removeChild(loadingIndicator);
            const result = await response.json();

            if (response.ok) {
                displayAiResponse(result.answer, result.source_context);
            } else {
                throw new Error(result.error || 'Failed to get an answer.');
            }

        } catch (error) {
            if (chatMessages.contains(loadingIndicator)) {
                chatMessages.removeChild(loadingIndicator);
            }
            appendMessage(`Error: ${error.message}`, 'ai');
        }
    });

    function appendMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${sender}-message`);
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return messageDiv;
    }

    function displayAiResponse(answer, source) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', 'ai-message');
        
        const answerP = document.createElement('p');
        answerP.classList.add('answer');
        answerP.textContent = answer;
        
        const sourceHeader = document.createElement('h4');
        sourceHeader.textContent = 'Source Context:';
        
        const sourcePre = document.createElement('pre');
        sourcePre.classList.add('source');
        sourcePre.textContent = source;
        
        messageDiv.appendChild(answerP);
        messageDiv.appendChild(sourceHeader);
        messageDiv.appendChild(sourcePre);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});