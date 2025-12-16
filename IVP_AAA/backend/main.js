const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from frontend directory
app.use(express.static(path.join(__dirname, '../frontend')));

// Serve images from any local path (for CORS fix)
app.get('/image/*', (req, res) => {
    const imagePath = req.params[0];
    const fullPath = path.resolve(imagePath);
    
    // Security check - only allow certain directories
    if (!fullPath.startsWith('C:\\') && !fullPath.startsWith('/')) {
        return res.status(403).send('Access denied');
    }
    
    if (fs.existsSync(fullPath)) {
        res.sendFile(fullPath);
    } else {
        res.status(404).send('Image not found');
    }
});

// Set proper MIME types
app.use((req, res, next) => {
    if (req.url.endsWith('.css')) {
        res.setHeader('Content-Type', 'text/css');
    } else if (req.url.endsWith('.js')) {
        res.setHeader('Content-Type', 'application/javascript');
    } else if (req.url.endsWith('.html')) {
        res.setHeader('Content-Type', 'text/html');
    }
    next();
});

// Global variables
let currentAnalysis = null;
let analysisProcess = null;

// Load topics from Topic.json
function loadTopics() {
    try {
        const topicsData = fs.readFileSync(path.join(__dirname, '../Topic.json'), 'utf8');
        return JSON.parse(topicsData);
    } catch (error) {
        console.error('Error loading topics:', error);
        return { Image_Topics: [], Video_Topics: [] };
    }
}

// Load analyser data
function loadAnalyserData() {
    try {
        const filePath = path.join(__dirname, '../Analyser.json');
        console.log('Loading analyser data from:', filePath);
        
        if (!fs.existsSync(filePath)) {
            console.warn('Analyser.json file not found, returning empty array');
            return [];
        }
        
        const data = fs.readFileSync(filePath, 'utf8');
        const parsed = JSON.parse(data);
        
        // Validate that it's an array
        if (!Array.isArray(parsed)) {
            console.error('Analyser.json does not contain an array, returning empty array');
            return [];
        }
        
        console.log(`Loaded ${parsed.length} analyses from Analyser.json`);
        return parsed;
    } catch (error) {
        console.error('Error loading analyser data:', error);
        return [];
    }
}

// Save analyser data
function saveAnalyserData(data) {
    try {
        fs.writeFileSync(path.join(__dirname, '../Analyser.json'), JSON.stringify(data, null, 2));
        return true;
    } catch (error) {
        console.error('Error saving analyser data:', error);
        return false;
    }
}

// Routes

// Get topics based on media type
app.get('/api/topics/:mediaType', (req, res) => {
    try {
        const { mediaType } = req.params;
        const topics = loadTopics();
        
        if (mediaType === 'image') {
            res.json({ topics: topics.Image_Topics });
        } else if (mediaType === 'video') {
            res.json({ topics: topics.Video_Topics });
        } else {
            res.status(400).json({ error: 'Invalid media type' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to load topics' });
    }
});

// Get all past analyses
app.get('/api/analyses', (req, res) => {
    try {
        console.log('GET /api/analyses - Request received');
        const analyses = loadAnalyserData();
        console.log(`Returning ${analyses.length} analyses to client`);
        res.json({ analyses });
    } catch (error) {
        console.error('Error in /api/analyses:', error);
        res.status(500).json({ error: 'Failed to load analyses', details: error.message });
    }
});

// Get specific analysis
app.get('/api/analyses/:id', (req, res) => {
    try {
        const { id } = req.params;
        const analyses = loadAnalyserData();
        const analysisId = parseInt(id) - 1; // Convert to 0-based index
        
        if (analysisId >= 0 && analysisId < analyses.length) {
            res.json({ analysis: analyses[analysisId] });
        } else {
            res.status(404).json({ error: 'Analysis not found' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to load analysis' });
    }
});

// Start new analysis
app.post('/api/analyze', (req, res) => {
    console.log('Received analysis request:', req.body);
    try {
        const { mediaType, topics, folderPath } = req.body;
        
        // Validate inputs
        if (!mediaType || !topics || !folderPath) {
            console.error('Missing required parameters:', { mediaType, topics, folderPath });
            return res.status(400).json({ error: 'Missing required parameters' });
        }
        
        if (!Array.isArray(topics) || topics.length === 0) {
            console.error('Invalid topics array:', topics);
            return res.status(400).json({ error: 'At least one topic must be selected' });
        }
        
        // Check if folder exists
        if (!fs.existsSync(folderPath)) {
            console.error('Folder path does not exist:', folderPath);
            return res.status(400).json({ error: 'Folder path does not exist' });
        }
        
        console.log('Validation passed, starting analysis...');
        
        // Stop current analysis if running
        if (analysisProcess) {
            console.log('Stopping current analysis...');
            analysisProcess.kill();
            analysisProcess = null;
        }
        
        // Start new analysis
        currentAnalysis = {
            mediaType,
            topics,
            folderPath,
            status: 'running',
            startTime: new Date().toISOString()
        };
        
        console.log('Current analysis set:', currentAnalysis);
        
        // Spawn Python process
        const pythonCommand = 'python';
        const pythonArgs = [
            path.join(__dirname, '../main.py'),
            mediaType,
            JSON.stringify(topics),
            folderPath
        ];
        const pythonOptions = {
            cwd: path.join(__dirname, '..')
        };
        
        console.log('Spawning Python process with:', {
            command: pythonCommand,
            args: pythonArgs,
            cwd: pythonOptions.cwd
        });
        
        const pythonProcess = spawn(pythonCommand, pythonArgs, pythonOptions);
        analysisProcess = pythonProcess;
        
        let output = '';
        let error = '';
        
        pythonProcess.stdout.on('data', (data) => {
            const dataStr = data.toString();
            output += dataStr;
            console.log('Python stdout:', dataStr);
        });
        
        pythonProcess.stderr.on('data', (data) => {
            const dataStr = data.toString();
            error += dataStr;
            console.error('Python stderr:', dataStr);
        });
        
        pythonProcess.on('close', (code) => {
            analysisProcess = null;
            console.log(`Python process closed with code: ${code}`);
            console.log(`Output: ${output}`);
            console.log(`Error: ${error}`);
            
            if (code === 0) {
                try {
                    // Extract JSON from output (remove any non-JSON content)
                    let jsonOutput = output.trim();
                    
                    // Find the JSON part (look for { and })
                    const jsonStart = jsonOutput.indexOf('{');
                    const jsonEnd = jsonOutput.lastIndexOf('}');
                    
                    if (jsonStart !== -1 && jsonEnd !== -1 && jsonEnd > jsonStart) {
                        jsonOutput = jsonOutput.substring(jsonStart, jsonEnd + 1);
                    }
                    
                    const result = JSON.parse(jsonOutput);
                    currentAnalysis.status = 'completed';
                    currentAnalysis.result = result;
                    currentAnalysis.endTime = new Date().toISOString();
                    
                    // Note: Analysis data is already saved by the Python script
                    console.log('Analysis completed successfully');
                    // Don't send response here as it was already sent
                } catch (parseError) {
                    currentAnalysis.status = 'error';
                    currentAnalysis.error = 'Failed to parse analysis result';
                    console.error('Failed to parse analysis result:', parseError);
                    console.error('Raw output:', output);
                    console.error('Extracted JSON:', jsonOutput);
                    // Don't send response here as it was already sent
                }
            } else {
                currentAnalysis.status = 'error';
                currentAnalysis.error = error || 'Analysis failed';
                console.error('Analysis failed with code:', code);
                console.error('Error details:', error);
                // Don't send response here as it was already sent
            }
        });
        
        // Send immediate response
        res.json({ 
            success: true, 
            message: 'Analysis started',
            analysisId: currentAnalysis.startTime
        });
        
    } catch (error) {
        console.error('Error starting analysis:', error);
        res.status(500).json({ error: 'Failed to start analysis' });
    }
});

// Stop current analysis
app.post('/api/stop-analysis', (req, res) => {
    try {
        if (analysisProcess) {
            analysisProcess.kill();
            analysisProcess = null;
            currentAnalysis = null;
            res.json({ success: true, message: 'Analysis stopped' });
        } else {
            res.json({ success: true, message: 'No analysis running' });
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to stop analysis' });
    }
});

// Get analysis status
app.get('/api/analysis-status', (req, res) => {
    try {
        if (currentAnalysis) {
            res.json({ 
                analysis: currentAnalysis,
                isRunning: analysisProcess !== null
            });
        } else {
            res.json({ 
                analysis: null,
                isRunning: false
            });
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to get analysis status' });
    }
});

// Get analysis summary
app.get('/api/summary', (req, res) => {
    try {
        const analyses = loadAnalyserData();
        
        if (analyses.length === 0) {
            return res.json({ summary: 'No analyses performed yet.' });
        }
        
        let summary = `Total Analyses: ${analyses.length}\n\n`;
        
        analyses.forEach((analysis, index) => {
            const goodCount = analysis.output.good_images.length;
            const badCount = analysis.output.bad_images.length;
            const total = goodCount + badCount;
            
            summary += `Analysis ${index + 1}:\n`;
            summary += `  Type: ${analysis.selected}\n`;
            summary += `  Folder: ${path.basename(analysis.folder_path)}\n`;
            summary += `  Results: ${goodCount} good, ${badCount} bad\n`;
            summary += `  Quality: ${total > 0 ? (goodCount/total*100).toFixed(1) : 0}%\n\n`;
        });
        
        res.json({ summary });
    } catch (error) {
        res.status(500).json({ error: 'Failed to generate summary' });
    }
});

// Serve frontend
app.get('/', (req, res) => {
    res.setHeader('Content-Type', 'text/html');
    res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Handle 404 for static files
app.use((req, res, next) => {
    if (req.url.startsWith('/api/')) {
        return next();
    }
    res.status(404).send('File not found');
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Something went wrong!' });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log('IVP AI Photographer Analyzer Backend is ready!');
});

// Graceful shutdown
process.on('SIGINT', () => {
    console.log('\nShutting down server...');
    if (analysisProcess) {
        analysisProcess.kill();
    }
    process.exit(0);
});
