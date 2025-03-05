import React, { useState, useEffect } from 'react';
import styles from '../styles/JDEditor.module.css'; 

function JDEditor({tempapi}) {
    const [currentJobIndex, setCurrentJobIndex] = useState(0);
    const [jobList, setJobList] = useState();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [currentJob, setCurrentJob] = useState();
    const [saved, setSaved] = useState(false)

    // Fetch JD data from backend
    useEffect(() => {
        const fetchJobDesc = async () => {
            try {
                const response = await tempapi.get('/jds/get-jd-list'); 
                
                const jdList = response.data.jobDescription
                console.log("response got----->", jdList)
                setJobList(jdList);
                console.log("job list ----->", jdList)
                console.log("-=-=-==-", jdList.length)
                console.log("==========>", jdList[0])
                setCurrentJob(jdList[0])
                // console.log("current job====", currentJob)
                setLoading(false);
            } catch (err) {
                setError(`Failed to fetch job Desc: ${err.message}`);
                setLoading(false);
            }
        };
        fetchJobDesc();
    }, []); 

    const handleInputChange = (e) => {
        console.log("handle input change====>",e)
        console.log("e.target :", e.target)

        const { name, value } = e.target;

        setCurrentJob(prevJob => ({
            ...prevJob,
            [name]: name === 'resumeGenerated' ? value === 'true' : value,
    }))};


    const handleDelete = async () => {

        console.log("...........", jobList)
        console.log("current job======>", currentJob)
        console.log("current index ---->", currentJobIndex)
        const newList =jobList.filter((_,index) => index !== currentJobIndex )
        console.log("=====newList ----->", newList)

        saveJD(newList)
        
        if (saved) {
            alert('Job desc deleted successfully!');
            console.log("Deleted Job:", currentJob);
            console.log("Deleted Job Descriptions Array (for demonstration):", updatedJobDescriptions);
        }       
    };

    const saveJD = async (updatedJD) => {

        try {
            console.log("updatedJD----->", updatedJD)
            const response = await tempapi.put('/jds/save-jobdesc', 
            {
                jobDescription: updatedJD
            });
            console.log('Success:', response);
          } catch (error) {
            console.error('Error:', error);
          }

    };


    const handleSave = async () => {
        // In a real application, you would handle saving to a backend or local storage here.
        // For now, we will just update the jobDescriptions array (immutably for React).
        // This example demonstrates updating the state, but you'd need to integrate with your data storage.

        // Create a copy of jobDescriptions to avoid direct mutation
        const updatedJobDescriptions = [...jobList];
        updatedJobDescriptions[currentJobIndex] = { ...currentJob };
        console.log(updatedJobDescriptions)
        // In a real app, instead of just logging, you would likely:
        // 1. Update the jobDescriptions array in the parent component's state if it's passed as props
        // 2. Or call an API to save the data to a backend, and then update the local state upon success.

        saveJD(updatedJobDescriptions)
        if (saved) {
            alert('Job desc saved successfully!');
            console.log("Saved Job:", currentJob);
            console.log("Updated Job Descriptions Array (for demonstration):", updatedJobDescriptions);
        }
    };

    const handleNextJob = () => {
        if (currentJobIndex < jobList.length - 1) {
            const nextIndex = currentJobIndex + 1;
            setCurrentJobIndex(nextIndex);
            setCurrentJob({ ...jobList[nextIndex] });
        } else {
            alert("You are at the last Job Description.");
        }
    };

    const handlePreviousJob = () => {
        if (currentJobIndex > 0) {
            const prevIndex = currentJobIndex - 1;
            setCurrentJobIndex(prevIndex);
            setCurrentJob({ ...jobList[prevIndex] });
        } else {
            alert("You are at the first Job Description.");
        }
    };

    // if (jobList.length === 0) {
    //     return <div>No job descriptions available.</div>; // Handle empty list case
    // }

    if (loading) {
        return <div>Loading resume...</div>;
    }

    if (error) {
        return <div style={{ color: 'red' }}>Error: {error}</div>;
    }



    return (
        <div className={styles.jdeditor} id="editorContainer">
            <h1>Job Description Editor</h1>
                <section>
                    <h2>Job {currentJobIndex + 1} / {jobList.length}</h2>
                    <table>
                        <tbody>
                            <tr>
                                <td>Company:</td>
                                <td>
                                    <input
                                        type="text"
                                        id="company"
                                        name="company"
                                        value={currentJob.company}
                                        onChange={handleInputChange}
                                    />
                                </td>
                            </tr>
                            <tr>
                                <td>Job Title:</td>
                                <td>
                                    <input
                                        type="text"
                                        id="title"
                                        name="jobTitle"
                                        value={currentJob.jobTitle}
                                        onChange={handleInputChange}
                                    />
                                </td>
                            </tr>
                            <tr>
                                <td>Job Link:</td>
                                <td>
                                    <input
                                        type="text"
                                        id="link"
                                        name="jobLink"
                                        value={currentJob.jobLink}
                                        onChange={handleInputChange}
                                    />
                                </td>
                            </tr>                                                        
                            <tr>
                                <td>Location:</td>
                                <td>
                                    <input
                                        type="text"
                                        id="location"
                                        name="jobLocation"
                                        value={currentJob.jobLocation}
                                        onChange={handleInputChange}
                                    />
                                </td>
                            </tr>
                            <tr>
                                <td>Resume Generated:</td>
                                <td>
                                <select name='resumeGenerated' 
                                         value={currentJob.resumeGenerated }
                                        onChange={handleInputChange} >
                                    <option value={"true"}>True</option>                                            
                                    <option value={"false"}>False</option>
                                </select>
                                </td>
                            </tr>
                            <tr>
                                <td>Job Description:</td>
                                <td>
                                    <textarea
                                        id="jobDesc"
                                        name="jobDesc"
                                        value={currentJob.jobDesc}
                                        onChange={handleInputChange}
                                    />
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <div style={{ marginTop: '10px', textAlign: 'right' }}>
                        <button onClick={handleDelete}>
                            Delete
                        </button>
                        <button onClick={handlePreviousJob} disabled={currentJobIndex === 0}>
                            Previous
                        </button>
                        <button  onClick={handleNextJob} disabled={currentJobIndex === jobList.length - 1}>
                            Next
                        </button>
                        <button  onClick={handleSave}>
                            Save
                        </button>
                    </div>
                </section>
        </div>
    );

};
export default JDEditor;