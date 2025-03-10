import React, { useState, useEffect } from 'react';
import styles from '../styles/Editor.module.css'; 

function ResumeEditor({tempapi, selectedResumeId}) {
    // const [ api, setApi] = useState(null)
    const [resumeData, setResumeData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState('');
    // Local state for temporary responsibilities input
    const [tempResponsibilities, setTempResponsibilities] = useState('');

    // Fetch resume data from backend
    useEffect(() => {
        const fetchResume = async () => {
            try {
                // console.log("inside the fetchResume method", tempapi)
                // setApi (tempapi)
                console.log("{selectedResumeName}-------", selectedResumeId)
                const response = await tempapi.get(`/resumes/get-json-resume/${selectedResumeId}`); 
                console.log("response got----->", response)
                setResumeData(response.data);
                setLoading(false);
            } catch (err) {
                setError(`Failed to fetch resume: ${err.message}`);
                setLoading(false);
            }
        };

        fetchResume();
    }, []);   // Empty dependency array: only run once on mount


    // Function to update a value in the resume data
    const handleInputChange = (section, field, value) => {
        setResumeData(prevData => ({
            ...prevData,
            [section]: {
                ...prevData[section],
                [field]: value
            }
        }));
    };
    
    // Handler to update the temporary responsibilities for a specific experience
    const handleTempResponsibilitiesChange = (index, value) => {
        console.log(index,"---", value)
        setTempResponsibilities((prev) => ({
        ...prev,
        [index]: value,
        }));
    };


    // Handler to update the main state
    const handleUpdate = (index) => {
        const inputValue = tempResponsibilities;
        console.log("tempResp--", inputValue)
        // Extract quoted items
        const quotedMatches = inputValue[index].match(/"(.*?)"/g) || [];
        console.log("quotedmatches---", quotedMatches)
        const quotedItems = quotedMatches.map(match => match.slice(1, -1));
        console.log("quoted items ----", quotedItems)
        // Extract non-quoted items (split by commas and trim)
        const nonQuotedItems = inputValue[index]
        .split(',\n') // Split by commas
        .map(item => item.trim()) // Trim whitespace
        .filter(item => !item.match(/^".*"$/)); // Exclude items already captured in quotedItems

        console.log("non quoted items -----", nonQuotedItems)
        // Combine quoted and non-quoted items
        const responsibilitiesArray = [...quotedItems, ...nonQuotedItems].filter(Boolean);
        console.log("responsibilities Array -----", responsibilitiesArray)

        setResumeData(prevData => {
            const section ="experiences"
            const field = "responsibilities"
            console.log("prev data====>", prevData[section])
            const updatedSection = [...prevData[section]];  // Create a copy of array
            console.log("updated Section ....1", updatedSection)
            updatedSection[index] = {
                ...updatedSection[index],
                [field]: responsibilitiesArray
            };
            console.log("updated Section ....2", updatedSection)
            // setTempResponsibilities("")
            return {
                ...prevData,
                [section]: updatedSection
            };
        });
    };

    // Generic function to update array elements
    const handleArrayItemChange = (section, index, field, value) => {
        console.log("section ===>", section)
        console.log("index====>", index)
        console.log("field===>", field)
        console.log("value====>", value)
        setResumeData(prevData => {
            console.log("prev data====>", prevData[section])
            const updatedSection = [...prevData[section]];  // Create a copy of array
            console.log("updated Section ....1", updatedSection)
            updatedSection[index] = {
                ...updatedSection[index],
                [field]: value
            };
            console.log("updated Section ....2", updatedSection)

            return {
                ...prevData,
                [section]: updatedSection
            };
        });
    };



    // Function to add a new item to an array section
    const handleAddItem = (section) => {
        setResumeData(prevData => ({
            ...prevData,
            [section]: [{},...prevData[section]]  // Add an empty object
        }));
    };

    // Function to remove an item from an array section
    const handleRemoveItem = (section, index) => {
        setResumeData(prevData => ({
            ...prevData,
            [section]: prevData[section].filter((_, i) => i !== index)
        }));
    };

    // Function to save the resume data to the backend
    const handleSaveAndGen = async () => {
        setIsProcessing(true)
        try {
            console.log("inside the handle save method", selectedResumeId)
            await tempapi.put(`/resumes/save-resume/${selectedResumeId}`, resumeData); 
            alert('Resume saved successfully!');
            setIsProcessing(false)
        } catch (err) {
            setError(`Failed to save resume: ${err.message}`);
            setIsProcessing(false)
        }
    };


    if (loading) {
        return <div>Loading resume...</div>;
    }

    if (error) {
        return <div style={{ color: 'red' }}>Error: {error}</div>;
    }

    if (!resumeData) {
        return <div>No resume data available.</div>;
    }

    return (
        <div className={styles.editor}>
            <h1>Resume Editor</h1>

            {/* SECTION: Personal Information */}
            <section className={styles.section}>
            <h2>Personal Information</h2>
                <table>
                    <tbody>
                    <tr>
                        <td><label>Name: </label></td> 
                        <td><input type="text" value={resumeData.personalDetails.name || ''} onChange={(e) => handleInputChange('personalDetails', 'name', e.target.value)} autoComplete="off"/>
                        </td>
                        <td><label>Email Id: </label></td> 
                        <td><input type="text" value={resumeData.personalDetails.email || ''} onChange={(e) => handleInputChange('personalDetails', 'email', e.target.value)} autoComplete="off"/>
                        </td>
                    </tr>
                    <tr>
                        <td><label>Mobile No: </label></td>
                        <td><input type="text" value={resumeData.personalDetails.mobile || ''} onChange={(e) => handleInputChange('personalDetails', 'mobile', e.target.value)} autoComplete="off"/>
                        </td>
                        <td><label>Location: </label></td> 
                        <td><input type="text" value={resumeData.personalDetails.location || ''} onChange={(e) => handleInputChange('personalDetails', 'location', e.target.value)} autoComplete="off"/>
                        </td>
                    </tr>
                    <tr>
                        <td><label>GitHub: </label></td> 
                        <td><input type="text" value={resumeData.personalDetails.github || ''} onChange={(e) => handleInputChange('personalDetails', 'github', e.target.value)} autoComplete="off"/>
                        </td>
                        <td><label>LinkedIn: </label></td> 
                        <td><input type="text" value={resumeData.personalDetails.linkedin || ''} onChange={(e) => handleInputChange('personalDetails', 'linkedin', e.target.value)} autoComplete="off"/>
                        </td>
                    </tr>
                    <tr>
                        <td><label>Country: </label></td> 
                        <td><input type="text" value={resumeData.personalDetails.country || ''} onChange={(e) => handleInputChange('personalDetails', 'country', e.target.value)} autoComplete="off"/>
                        </td>
                    </tr>

                    </tbody>
                </table>
            </section>

            {/* SECTION: Summary section  */}
            <section className={styles.section}>
                <h2>Summary</h2>
                <textarea value={resumeData.summary.summary || ''} onChange={(e) => handleInputChange('summary', 'summary', e.target.value)} />
            </section>
            {/* SECTION: Education (Similar structure to Experience) */}
            <section className={styles.section}>
                <h2>Education</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Sr.No.</th>
                                <th>Institution</th>
                                <th>Degree</th>
                                <th>Field of Study</th>
                                <th>Duration</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {resumeData.education.map((edu, index) => (
                            <tr key={index}>
                                <td>{index + 1}</td>
                                <td><input type="text" value={edu.institution || ''} onChange={(e) => handleArrayItemChange('education', index, 'institution', e.target.value)} />
                                </td>
                                <td><input type="text" value={edu.degree || ''} onChange={(e) => handleArrayItemChange('education', index, 'degree', e.target.value)} />
                                </td>
                                <td><input type="text" value={edu.field_of_study || ''} onChange={(e) => handleArrayItemChange('education', index, 'field_of_study', e.target.value)} />
                                </td>
                                <td><input type="text" value={edu.duration || ''} onChange={(e) => handleArrayItemChange('education', index, 'duration', e.target.value)} />
                                </td>
                                <td>
                                    <button className={styles.btn} onClick={() => handleRemoveItem('education', index)}>Remove</button>
                                </td>
                            </tr>
                            ))}
                        </tbody>
                    </table>
                    <button onClick={() => handleAddItem('education')}>Add Education</button>
            </section>
            {/* Experience section*/}
            <section className={styles.section}>
                <h2>Experience</h2>
                <table>
                    <thead>
                        <tr>
                            <th></th>
                            <th>Company</th>
                            <th>Title</th>
                            <th>Duration</th>
                            <th></th>
                        </tr>
                    </thead>
                    {resumeData.experiences.map((exp, index) => (
                    <tbody key={index}>
                        <tr>
                            <td>{index + 1}</td>
                            <td>
                                <input type="text" value={exp.company || ''} onChange={(e) => handleArrayItemChange('experiences', index, 'company', e.target.value)} />
                            </td>
                            <td>
                                <input type="text" value={exp.position || ''} onChange={(e) => handleArrayItemChange('experiences', index, 'position', e.target.value)} />
                            </td>
                            <td>
                                <input type="text" value={exp.duration || ''} onChange={(e) => handleArrayItemChange('experiences', index, 'duration', e.target.value)} />
                            </td>
                            <td>
                                <button onClick={() => handleRemoveItem('experiences', index)}>Remove</button>
                            </td>
                        </tr>
                        <tr>
                            <th colSpan={5}>Responsibilities:</th>
                        </tr>
                        <tr>
                            <td colSpan={4}>
                            <textarea 
                                value={tempResponsibilities[index] ||(Array.isArray(exp.responsibilities)
                                    ? exp.responsibilities.map(resp => `"${resp}"`).join(',\n')
                                    : '')}
                                onChange={(e) => handleTempResponsibilitiesChange(index, e.target.value)}                   />
                            </td>
                            <td>
                                <button onClick={() => handleUpdate(index)}>Update</button>
                            </td>
                        </tr>
                    </tbody>
                    ))}
                </table>

                <div>
                    <button onClick={() => handleAddItem('experiences')}>Add Experience</button>
                </div>
            </section>

            {/* SECTION: Achievements */}
            {resumeData.achievements ? 
            <section className={styles.section}>
                <h2>Achievements</h2>
                <table>
                    <thead>
                        <tr>
                            <th></th>
                            <th>Name</th>
                            <th>Description</th>
                            <th></th>
                        </tr>
                    </thead>
                    {resumeData.achievements.map((achievements, index) => (
                    <tbody key={index}>
                        <tr >
                            <td>{index + 1}</td>
                            <td><input type="text" value={achievements.name || ''} onChange={(e) => handleArrayItemChange('achievements', index, 'name', e.target.value)}/>
                            </td>
                            <td><input type="text" value={achievements.description || ''} onChange={(e) => handleArrayItemChange('achievements', index, 'description', e.target.value)}/>
                            </td>
                            <td>
                                <button onClick={() => handleRemoveItem('achievements', index)}>Remove</button>
                            </td>
                        </tr>
                    </tbody>
                    ))}
                </table>
                <button onClick={() => handleAddItem('achievements')}>Add Achievements</button>
            </section>
            : "" }

            {/* SECTION: Certifications */}
            <section className={styles.section}>
                <h2>Certifications</h2>
                <table>
                    <thead>
                        <tr>
                            <th></th>
                            <th>Name</th>
                            <th>Description</th>
                            <th></th>
                        </tr>
                    </thead>
                    {resumeData.certifications.map((certification, index) => (
                    <tbody key={index}>
                        <tr >
                            <td>{index + 1}</td>
                            <td><input type="text" value={certification.name || ''} onChange={(e) => handleArrayItemChange('certifications', index, 'name', e.target.value)}/>
                            </td>
                            <td><input type="text" value={certification.description || ''} onChange={(e) => handleArrayItemChange('certifications', index, 'description', e.target.value)}/>
                            </td>
                            <td>
                                <button onClick={() => handleRemoveItem('certifications', index)}>Remove</button>
                            </td>
                        </tr>
                    </tbody>
                    ))}
                </table>
                <button onClick={() => handleAddItem('certifications')}>Add Certifications</button>
            </section>

            {/* SECTION: Skills */}
            <section className="section">
                    <h2>Skills</h2>
                    <table>
                        <thead>
                            <tr>
                                <th></th>
                                <th>Skill</th>
                                <th>Description</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                        {resumeData.skills.map((skill, index) => (
                            <tr key = {index}>
                                <td>{index + 1}</td>
                                <td>
                                    <input type="text" value={skill.name || ''} onChange={(e) => handleArrayItemChange('skills', index, 'name', e.target.value)}/>
                                </td>
                                <td>
                                    <textarea className={styles.classtextarea} value={skill.description || ''} onChange={(e) => handleArrayItemChange('skills', index, 'description', e.target.value)}/>
                                </td>
                                <td>
                                    <button onClick={() => handleRemoveItem('skills', index)}>Remove</button>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                    <button onClick={() => handleAddItem('skills')}>Add Skill</button>
            </section>
            <section>
                <button onClick={handleSaveAndGen} disabled={isProcessing}>
                {isProcessing ? '...Saving the Resume' : 'Save JSON and Generate PDF'}
                </button>
            </section>
        </div>
    );
}

export default ResumeEditor;
