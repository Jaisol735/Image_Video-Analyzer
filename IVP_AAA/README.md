# IVP AI Photographer Analyzer

An AI-powered professional photographer analyzer that uses 30 different Image and Video Processing (IVP) techniques to evaluate the quality of images and videos.

## Features

- **Multi-Modal Analysis**: Supports both image and video analysis
- **30 IVP Topics**: Comprehensive analysis using various computer vision techniques
- **AI-Powered Evaluation**: Uses Google Gemini AI for intelligent quality assessment
- **Beautiful UI**: Modern, responsive interface with smooth animations
- **Real-time Processing**: Live progress tracking during analysis
- **Results Management**: Store and view past analysis results
- **Detailed Reports**: Get comprehensive summaries and quality scores

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Google Gemini API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd IVP_AAA
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Gemini API**
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the API key in `main.py`:
     ```python
     genai.configure(api_key="YOUR_GEMINI_API_KEY")
     ```

## Usage

1. **Start the backend server**
   ```bash
   npm start
   ```

2. **Open your browser**
   Navigate to `http://localhost:3000`

3. **Start analyzing**
   - Select media type (Images or Videos)
   - Choose analysis topics from the available IVP modules
   - Provide folder path containing your media files
   - Click "Start Analysis" and wait for results

## Available IVP Topics

### Image Topics
- Digital Image Representation
- Distance Measures and File Formats
- Point Processing Linear Negative
- Contrast Stretching
- Thresholding and Intensity Slicing
- Log Transformation
- Power Law Transformation
- Smoothing Spatial Filters
- Sharpening and Gaussian Filtering
- Median Filtering
- Histogram Equalization
- Fourier Spectrum and Analysis
- Image Transforms
- Discrete Cosine Transform
- Dilation and Erosion
- Opening and Closing
- Hit or Miss Transformation
- Thinning and Thickening
- Grayscale Morphology
- Gradient Based Edge Detection
- Edge Detection Operators
- Pixel Relationships and Segmentation
- Bayesian Classification and Otsu Method
- Region Growing Segmentation
- Region Splitting and Merging
- Color Fundamentals and RGB Model
- Other Color Models
- Color Model Transformation
- Histogram Processing of Color Images
- Video Processing and Motion Estimation

### Video Topics
- Smoothing Spatial Filters
- Sharpening and Gaussian Filtering
- Median Filtering
- Histogram Equalization
- Fourier Spectrum and Analysis
- Image Transforms
- Discrete Cosine Transform
- Gradient Based Edge Detection
- Edge Detection Operators
- Color Fundamentals and RGB Model
- Other Color Models
- Color Model Transformation
- Histogram Processing of Color Images
- Video Processing and Motion Estimation

## Project Structure

```
IVP_AAA/
├── backend/
│   └── main.js              # Express.js backend server
├── frontend/
│   ├── index.html           # Main HTML interface
│   ├── script.js            # Frontend JavaScript
│   └── script.css           # Styling and animations
├── IVP_Modules/             # 30 IVP processing modules
├── main.py                  # Python processing engine
├── Topic.json               # Available topics configuration
├── Analyser.json            # Analysis results database
├── requirements.txt         # Python dependencies
├── package.json             # Node.js dependencies
└── README.md               # This file
```

## How It Works

1. **Media Selection**: User selects whether to analyze images or videos
2. **Topic Selection**: User chooses from 30 available IVP analysis topics
3. **Folder Input**: User provides path to folder containing media files
4. **Processing**: Each media file is processed through selected IVP modules
5. **AI Analysis**: Processed results are sent to Gemini AI for quality assessment
6. **Results**: Images/videos are classified as "Good" or "Bad" with reasoning
7. **Summary**: Comprehensive analysis summary is generated

## API Endpoints

- `GET /api/topics/:mediaType` - Get available topics for media type
- `GET /api/analyses` - Get all past analyses
- `GET /api/analyses/:id` - Get specific analysis details
- `POST /api/analyze` - Start new analysis
- `POST /api/stop-analysis` - Stop current analysis
- `GET /api/analysis-status` - Get current analysis status
- `GET /api/summary` - Get analysis summary

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.
