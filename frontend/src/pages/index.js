// pages/index.js
import { useState, useEffect } from 'react';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import styles from '../styles/Home.module.css';
import ResumeEditor from '../components/ResumeEditor';
import JDEditor from '../components/JDEditor'

export default function Home() {
  const [uploadedResume, setUploadedResume] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isResEditorVisible, setIsResEditorVisible] = useState(false);
  const [isJDEditorVisible, setIsJDEditorVisible] = useState(false);

  const toggleJDEditor = () => {
    setIsJDEditorVisible(!isJDEditorVisible);
};

  const toggleResEditor = () => {
      setIsResEditorVisible(!isResEditorVisible);
  };
  // Configure Axios to point to your Python backend
  // process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const api = axios.create({
    baseURL: 'http://localhost:8000',     
  });

  const handleFileUpload = async (file) => {
    setIsLoading(true);
    setError(null);
  
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/resumes/upload-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setUploadedResume(response.data);

    } catch (err) {
      setError('Failed to process resume. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1>AI Resume Generator</h1>
        {/* File upload section */}
        <div>
          <FileUpload onUpload={handleFileUpload} />
          {isLoading && <div className={styles.loading}>Uploading...</div>}
        </div>
        <div>
            {!isJDEditorVisible && (
            <button name="resumeEditor" className={styles.showButton} onClick={toggleResEditor}>
                {isResEditorVisible ? 'Hide Resume Editor' : 'Show Resume Editor'}
            </button> 
            )}
            { !isResEditorVisible && (
            <button name="jdEditor" className={styles.showButton} onClick={toggleJDEditor}>
                {isJDEditorVisible ? 'Hide JD Editor' : 'Show JD Editor'}
            </button>
            )}            
        </div>

        {isResEditorVisible && (
          <div>
              <ResumeEditor tempapi = {api} />
          </div>
        )}
        {isJDEditorVisible && (
          <div>
              <JDEditor tempapi = {api} />
          </div>
        )}



    </div>
  )
};