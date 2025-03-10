// pages/index.js
import { useState, useEffect } from 'react';
import axios from 'axios';
import FileUpload from '../components/FileUpload';
import styles from '../styles/Home.module.css';
import ResumeEditor from '../components/ResumeEditor';
import JDEditor from '../components/JDEditor'

export default function Home() {
  const [currentJobIndex, setCurrentJobIndex] = useState(0);
  const [jobList, setJobList] = useState([]);
  const [uploadedResume, setUploadedResume] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isResEditorVisible, setIsResEditorVisible] = useState(false);
  const [isJDEditorVisible, setIsJDEditorVisible] = useState(false);
  const [isJsonGenVisible, setIsJsonGenVisible] = useState(false);
  const [isPdfGenVisible, setIsPdfGenVisible] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false); 
  const [resumeList, setResumeList] = useState([])
  const [selectedResumeName, setSelectedResumeName] = useState(null); // Store the selected resume
  const [selectedJDName, setSelectedJDName] = useState(""); // Store the selected resume
  
  const [loading, setLoading] = useState(true);
  const toggleJDEditor = () => {
    setIsJDEditorVisible(!isJDEditorVisible);
  };
  const toggleResEditor = () => {
      setIsResEditorVisible(!isResEditorVisible);
  };

  const handlePdfGen = () => {
    setIsProcessing(true); 
    setIsPdfGenVisible(!isPdfGenVisible);
  };


  // Configure Axios to point to your Python backend
  // process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const api = axios.create({
    baseURL: 'http://localhost:8000',     
  });

    // Fetch JD data from backend
    useEffect(() => {
        const fetchJobDesc = async () => {
            try {
                const show = "showFiltered"
                const response = await api.get(`/jds/get-jd-list/${show}`); 
                
                const jdList = response.data.jobDescription
                console.log("response got----->", jdList)
                setJobList(jdList);
                console.log("job list ----->", jdList)
                console.log("-=-=-==-", jdList.length)
                console.log("==========>", jdList[0])
                setLoading(false);
            } catch (err) {
                setError(`Failed to fetch job Desc: ${err.message}`);
                setLoading(false);
            }
        };
        fetchJobDesc();
    }, []); 


  // Fetch resume data from backend
    useEffect(() => {
        const fetchAllResume = async () => {
            try {
                console.log("inside the fetchAllResume method")
                const response = await api.get('/resumes/get-all-resumes'); 
                console.log("response got----->", response)
                setResumeList(response.data);
                setLoading(false);
            } catch (err) {
                setError(`Failed to fetch all resumes: ${err.message}`);
                setLoading(false);
            }
        };
        fetchAllResume();
    }, []); 

  // Handle dropdown selection
  const handleResumeSelect = (event) => {
    const selectedId = event.target.value;
    console.log("selectedID------->", selectedId )
    setSelectedResumeName(selectedId);
  };

  // Handle dropdown selection
  const handleJDSelect = (event) => {
    const selectedName = event.target.value;
    console.log("selected Name------->", selectedName )
    setSelectedJDName(selectedName);
  };

  const handleJsonGen = async () => {
    setIsProcessing(true); 
    console.log("selectedJDName====>", selectedJDName)

    console.log(`/resumes/gen-json-resume-per-jd/${selectedJDName}`)
    const response = await api.get(`/resumes/gen-json-resume-per-jd/${selectedJDName}`); 
    console.log("response got----->", response)
    if (response == false ) {
      setError("Error occurred while generating the JSON")
    }
    setIsProcessing(false); 
  
  };

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
        {/* Dropdown to Select a JD */}
        <div className={styles.container}> 
          <h2>Select Job Description</h2>
          <select onChange={handleJDSelect} defaultValue="">
            <option value="" disabled>
              {jobList.length > 0 ? 'Select a job Description' : 'No job descriptions available'}
            </option>
            {/* Options for resumes from the database */}
            { jobList.map((job, index) => (
              <option key={index} 
                value={`${job.company.replace(/\s/g, "$")}_${job.jobTitle.replace(/\s/g, "$")}`}>
                Company: {job.company} Position: {job.jobTitle}
              </option>
            ))}
          </select>
          {error && <div className={styles.error}>{error}</div>}
        {/* </div> */}

        {/* Buttons for generating json resume and pdf resume */}
        {/* <div> */}
            <button name="jsongenerator" className={styles.showButton} onClick={handleJsonGen}
                        disabled= {isProcessing}>
                {isProcessing ? '...Processing' : 'JSON Generator'}
            </button> 
        </div>


        {/* Dropdown to Select a Resume */}
        <div className={styles.container}> 
          <h2>Select Resume</h2>
          <select onChange={handleResumeSelect} defaultValue="">
            <option value="" disabled>
              Select a resume
            </option>
            {/* Options for resumes from the database */}
            {resumeList.map((resume) => (
              <option key={resume.name} value={resume.name}>
                Resume Name: {resume.name}
              </option>
            ))}
          </select>
          {error && <div className={styles.error}>{error}</div>}
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
              <ResumeEditor tempapi = {api} selectedResumeId = {selectedResumeName}/>
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