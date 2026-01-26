import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Handle file selection
  const handleFileChange = (e) => {
    setSelectedFiles(e.target.files);
  };

  // Handle Form Submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    
    // Only append text if the user wrote something
    if (inputText) {
      formData.append('text_input', inputText);
    }
    
    // Only append files if the user selected them
    if (selectedFiles && selectedFiles.length > 0) {
      for (let i = 0; i < selectedFiles.length; i++) {
        formData.append('files', selectedFiles[i]);
      }
    }

    try {
      // Connecting to your Backend on Port 8080
      const response = await axios.post('/api/refine', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Error connecting to server. Is the backend running on port 8080?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>✨ AI Prompt Refiner</h1>
        <p>Transform messy ideas into structured technical requirements.</p>
      </header>

      <main className="main-content">
        <div className="input-section">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Describe your idea:</label>
              <textarea 
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="e.g., I want an Uber-like app for tractors..."
                rows="4"
              />
            </div>

            <div className="form-group">
              <label>Upload Sketches or Docs (Optional):</label>
              <input 
                type="file" 
                multiple 
                onChange={handleFileChange}
                accept="image/*,.pdf"
              />
            </div>

            <button type="submit" disabled={loading || (!inputText && !selectedFiles)}>
              {loading ? 'Refining...' : 'Refine Prompt 🚀'}
            </button>
          </form>
          {error && <p className="error">{error}</p>}
        </div>

        {result && (
          <div className="output-section">
            <h2>🎯 Refined Output</h2>
            
            <div className="card">
              <h3>Core Intent</h3>
              <p><strong>Summary:</strong> {result.core_intent?.summary}</p>
              <p><strong>Goal:</strong> {result.core_intent?.primary_goal}</p>
              <p><strong>Audience:</strong> {result.core_intent?.target_audience}</p>
            </div>

            <div className="card">
              <h3>Specifications</h3>
              <div className="tags">
                <strong>Functional Requirements:</strong>
                <ul>
                  {result.specifications?.functional_requirements?.map((req, i) => (
                    <li key={i}>{req}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="json-preview">
              <details>
                <summary>View Raw JSON (For Developers)</summary>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </details>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;