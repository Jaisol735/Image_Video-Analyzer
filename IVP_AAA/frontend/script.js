// Global variables
let currentMediaType = null;
let selectedTopics = [];
let currentAnalysis = null;
let pastAnalyses = [];

// DOM elements
const elements = {
    sidebar: document.getElementById('sidebar'),
    mainContent: document.getElementById('mainContent'),
    welcomeScreen: document.getElementById('welcomeScreen'),
    topicSelection: document.getElementById('topicSelection'),
    folderInput: document.getElementById('folderInput'),
    analysisResults: document.getElementById('analysisResults'),
    pastAnalysisView: document.getElementById('pastAnalysisView'),
    pastAnalysisTitle: document.getElementById('pastAnalysisTitle'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    loadingStatus: document.getElementById('loadingStatus'),
    
    // Buttons
    newAnalysisBtn: document.getElementById('newAnalysisBtn'),
    imageBtn: document.getElementById('imageBtn'),
    videoBtn: document.getElementById('videoBtn'),
    backToMedia: document.getElementById('backToMedia'),
    backToTopics: document.getElementById('backToTopics'),
    backToWelcome: document.getElementById('backToWelcome'),
    proceedBtn: document.getElementById('proceedBtn'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    browseBtn: document.getElementById('browseBtn'),
    
    // Inputs
    folderPath: document.getElementById('folderPath'),
    folderFileInput: document.getElementById('folderFileInput'),
    
    // Content areas
    topicsGrid: document.getElementById('topicsGrid'),
    analysesList: document.getElementById('analysesList'),
    imagesGrid: document.getElementById('imagesGrid'),
    summaryContent: document.getElementById('summaryContent'),
    summaryText: document.getElementById('summaryText'),
    resultsStats: document.getElementById('resultsStats'),
    goodCount: document.getElementById('goodCount'),
    badCount: document.getElementById('badCount'),
    
    // Tabs
    goodImagesTab: document.getElementById('goodImagesTab'),
    badImagesTab: document.getElementById('badImagesTab'),
    summaryTab: document.getElementById('summaryTab')
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing application...');
    setupEventListeners();
    loadPastAnalyses();
    
    // Also try loading after a short delay in case of timing issues
    setTimeout(() => {
        if (pastAnalyses.length === 0 && elements.analysesList) {
            console.log('Retrying to load past analyses...');
            loadPastAnalyses();
        }
    }, 500);
});

// Setup event listeners
function setupEventListeners() {
    // Media type selection
    elements.imageBtn.addEventListener('click', () => selectMediaType('image'));
    elements.videoBtn.addEventListener('click', () => selectMediaType('video'));
    
    // Navigation buttons
    elements.backToMedia.addEventListener('click', showWelcomeScreen);
    elements.backToTopics.addEventListener('click', showTopicSelection);
    elements.backToWelcome.addEventListener('click', showWelcomeScreen);
    
    // New analysis
    elements.newAnalysisBtn.addEventListener('click', startNewAnalysis);
    
    // Proceed button
    elements.proceedBtn.addEventListener('click', showFolderInput);
    
    // Folder input
    elements.folderPath.addEventListener('input', validateFolderPath);
    elements.browseBtn.addEventListener('click', () => elements.folderFileInput.click());
    elements.folderFileInput.addEventListener('change', handleFolderSelection);
    
    // Analyze button
    elements.analyzeBtn.addEventListener('click', startAnalysis);
    
    // Tab switching
    elements.goodImagesTab.addEventListener('click', () => switchTab('good'));
    elements.badImagesTab.addEventListener('click', () => switchTab('bad'));
    elements.summaryTab.addEventListener('click', () => switchTab('summary'));
}

// Load past analyses from backend
async function loadPastAnalyses() {
    try {
        console.log('Loading past analyses...');
        const response = await fetch('/api/analyses');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Received analyses data:', data);
        
        pastAnalyses = data.analyses || [];
        console.log(`Loaded ${pastAnalyses.length} past analyses`);
        
        renderPastAnalyses();
    } catch (error) {
        console.error('Error loading past analyses:', error);
        // Show error to user
        if (elements.analysesList) {
            elements.analysesList.innerHTML = `
                <div class="no-analyses">
                    ⚠️
                    <p>Error loading analyses</p>
                    <small>Check console for details</small>
                </div>
            `;
        }
    }
}

// Render past analyses in sidebar
function renderPastAnalyses() {
    if (!elements.analysesList) {
        console.error('analysesList element not found!');
        return;
    }
    
    console.log(`Rendering ${pastAnalyses.length} past analyses`);
    
    if (pastAnalyses.length === 0) {
        elements.analysesList.innerHTML = `
            <div class="no-analyses">
                📋
                <p>No analyses yet</p>
            </div>
        `;
        return;
    }
    
    try {
        elements.analysesList.innerHTML = pastAnalyses.map((analysis, index) => {
            // Validate analysis structure
            if (!analysis || !analysis.selected || !analysis.topics_selected || !analysis.output) {
                console.warn(`Invalid analysis at index ${index}:`, analysis);
                return '';
            }
            
            const goodCount = (analysis.output.good_images || []).length;
            const badCount = (analysis.output.bad_images || []).length;
            
            return `
                <div class="analysis-item" onclick="loadPastAnalysis(${index})">
                    <div class="analysis-info">
                        <h4>Analysis ${index + 1}</h4>
                        <p>${analysis.selected} - ${analysis.topics_selected.length} topics</p>
                        <small>${new Date().toLocaleDateString()}</small>
                    </div>
                    <div class="analysis-stats">
                        <span class="good-count">${goodCount}</span>
                        <span class="bad-count">${badCount}</span>
                    </div>
                </div>
            `;
        }).filter(html => html !== '').join('');
        
        console.log('Past analyses rendered successfully');
    } catch (error) {
        console.error('Error rendering past analyses:', error);
        elements.analysesList.innerHTML = `
            <div class="no-analyses">
                ⚠️
                <p>Error rendering analyses</p>
            </div>
        `;
    }
}

// Load and display past analysis
async function loadPastAnalysis(index) {
    try {
        console.log(`Loading past analysis ${index + 1}`);
        const response = await fetch(`/api/analyses/${index + 1}`);
        const data = await response.json();
        
        if (data.analysis) {
            currentAnalysis = data.analysis;
            showPastAnalysisView();
            renderAnalysisResults(currentAnalysis);
        } else {
            console.error('No analysis data received:', data);
            showNotification('Error loading analysis data', 'error');
        }
    } catch (error) {
        console.error('Error loading past analysis:', error);
        showNotification('Error loading analysis', 'error');
    }
}

// Show past analysis view
function showPastAnalysisView() {
    hideAllScreens();
    elements.pastAnalysisView.style.display = 'block';
    
    // Safety check for pastAnalysisTitle element
    if (elements.pastAnalysisTitle) {
        elements.pastAnalysisTitle.textContent = `Analysis ${pastAnalyses.indexOf(currentAnalysis) + 1}`;
    }
}

// Select media type
async function selectMediaType(type) {
    currentMediaType = type;
    
    try {
        const response = await fetch(`/api/topics/${type}`);
        const data = await response.json();
        renderTopics(data.topics);
        showTopicSelection();
    } catch (error) {
        console.error('Error loading topics:', error);
        showNotification('Error loading topics', 'error');
    }
}

// Render topics as checkboxes
function renderTopics(topics) {
    elements.topicsGrid.innerHTML = topics.map(topic => `
        <div class="topic-item">
            <input type="checkbox" id="topic-${topic}" value="${topic}" class="topic-checkbox">
            <label for="topic-${topic}">${topic}</label>
        </div>
    `).join('');
    
    // Add event listeners to checkboxes
    document.querySelectorAll('.topic-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateProceedButton);
    });
}

// Update proceed button state
function updateProceedButton() {
    const checkedTopics = document.querySelectorAll('.topic-checkbox:checked');
    selectedTopics = Array.from(checkedTopics).map(cb => cb.value);
    elements.proceedBtn.disabled = selectedTopics.length === 0;
}

// Show topic selection screen
function showTopicSelection() {
    hideAllScreens();
    elements.topicSelection.style.display = 'block';
}

// Show folder input screen
function showFolderInput() {
    hideAllScreens();
    elements.folderInput.style.display = 'block';
}

// Show welcome screen
function showWelcomeScreen() {
    hideAllScreens();
    elements.welcomeScreen.style.display = 'block';
    resetForm();
}

// Hide all screens
function hideAllScreens() {
    elements.welcomeScreen.style.display = 'none';
    elements.topicSelection.style.display = 'none';
    elements.folderInput.style.display = 'none';
    elements.analysisResults.style.display = 'none';
    elements.pastAnalysisView.style.display = 'none';
}

// Reset form
function resetForm() {
    currentMediaType = null;
    selectedTopics = [];
    currentAnalysis = null;
    elements.folderPath.value = '';
    elements.analyzeBtn.disabled = true;
    elements.proceedBtn.disabled = true;
}

// Validate folder path
function validateFolderPath() {
    const path = elements.folderPath.value.trim();
    elements.analyzeBtn.disabled = path.length === 0;
}

// Handle folder selection
function handleFolderSelection(event) {
    const files = event.target.files;
    if (files.length > 0) {
        // Get the folder path from the first file
        const folderPath = files[0].webkitRelativePath.split('/')[0];
        elements.folderPath.value = folderPath;
        validateFolderPath();
    }
}

// Start new analysis
function startNewAnalysis() {
    showWelcomeScreen();
}

// Start analysis
async function startAnalysis() {
    const folderPath = elements.folderPath.value.trim();
    
    if (!folderPath) {
        showNotification('Please enter a valid folder path', 'error');
        return;
    }
    
    showLoadingOverlay();
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mediaType: currentMediaType,
                topics: selectedTopics,
                folderPath: folderPath
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Start polling for results
            pollAnalysisStatus();
        } else {
            hideLoadingOverlay();
            showNotification(data.error || 'Analysis failed', 'error');
        }
    } catch (error) {
        hideLoadingOverlay();
        console.error('Error starting analysis:', error);
        showNotification('Error starting analysis', 'error');
    }
}

// Poll analysis status
async function pollAnalysisStatus() {
    try {
        const response = await fetch('/api/analysis-status');
        const data = await response.json();
        
        if (data.isRunning) {
            if (elements.loadingStatus) {
                elements.loadingStatus.textContent = `Processing ${currentMediaType}s...`;
            }
            setTimeout(pollAnalysisStatus, 2000);
        } else if (data.analysis && data.analysis.status === 'completed') {
            hideLoadingOverlay();
            currentAnalysis = data.analysis.result;
            showAnalysisResults();
            renderAnalysisResults(currentAnalysis);
            loadPastAnalyses(); // Refresh sidebar
        } else if (data.analysis && data.analysis.status === 'error') {
            hideLoadingOverlay();
            showNotification(data.analysis.error || 'Analysis failed', 'error');
        }
    } catch (error) {
        hideLoadingOverlay();
        console.error('Error polling status:', error);
        showNotification('Error checking analysis status', 'error');
    }
}

// Show loading overlay
function showLoadingOverlay() {
    elements.loadingOverlay.style.display = 'flex';
}

// Hide loading overlay
function hideLoadingOverlay() {
    elements.loadingOverlay.style.display = 'none';
}

// Show analysis results
function showAnalysisResults() {
    hideAllScreens();
    elements.analysisResults.style.display = 'block';
}

// Render analysis results
function renderAnalysisResults(analysis) {
    const goodImages = analysis.output.good_images || [];
    const badImages = analysis.output.bad_images || [];
    
    // Update counts
    elements.goodCount.textContent = goodImages.length;
    elements.badCount.textContent = badImages.length;
    
    // Update stats
    elements.resultsStats.innerHTML = `
        <div class="stat-item">
            <span class="stat-label">Total ${analysis.selected}s:</span>
            <span class="stat-value">${goodImages.length + badImages.length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Good:</span>
            <span class="stat-value good">${goodImages.length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Bad:</span>
            <span class="stat-value bad">${badImages.length}</span>
        </div>
        <div class="stat-item">
            <span class="stat-label">Quality Score:</span>
            <span class="stat-value">${((goodImages.length / (goodImages.length + badImages.length)) * 100).toFixed(1)}%</span>
        </div>
    `;
    
    // Render images
    renderImagesGrid(goodImages, 'good');
    
    // Render summary
    elements.summaryText.textContent = analysis.summary || 'No summary available.';
}

// Render images grid
function renderImagesGrid(images, type) {
    if (images.length === 0) {
        elements.imagesGrid.innerHTML = `
            <div class="no-images">
                <i class="fas fa-${type === 'good' ? 'thumbs-up' : 'thumbs-down'}"></i>
                <p>No ${type} images found</p>
            </div>
        `;
        return;
    }
    
    elements.imagesGrid.innerHTML = images.map(image => `
        <div class="image-card">
            <div class="image-preview">
                <img src="/image/${encodeURIComponent(image.image_path)}" alt="${image.image_name}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZGRkIi8+PHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZHk9Ii4zZW0iPkltYWdlPC90ZXh0Pjwvc3ZnPg=='">
            </div>
            <div class="image-info">
                <h4>${image.image_name}</h4>
                <p class="reason">${image.reason}</p>
            </div>
        </div>
    `).join('');
}

// Switch tabs
function switchTab(type) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    
    if (type === 'good') {
        elements.goodImagesTab.classList.add('active');
        elements.imagesGrid.style.display = 'grid';
        elements.summaryContent.style.display = 'none';
        renderImagesGrid(currentAnalysis.output.good_images, 'good');
    } else if (type === 'bad') {
        elements.badImagesTab.classList.add('active');
        elements.imagesGrid.style.display = 'grid';
        elements.summaryContent.style.display = 'none';
        renderImagesGrid(currentAnalysis.output.bad_images, 'bad');
    } else if (type === 'summary') {
        elements.summaryTab.classList.add('active');
        elements.imagesGrid.style.display = 'none';
        elements.summaryContent.style.display = 'block';
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Show with animation
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}
