import React, { useState, useEffect } from 'react';
import styles from '../styles/Editor.module.css'; 

function ResumeEditor({tempapi}) {
    // const [ api, setApi] = useState(null)
    const [resumeData, setResumeData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    // Fetch resume data from backend
    useEffect(() => {
        const fetchResume = async () => {
            try {
            //     console.log("inside the fetchResume method", tempapi)
                // setApi (tempapi)
                const response = await tempapi.get('/api/get-json-resume'); 
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

    // Generic function to update array elements
    const handleArrayItemChange = (section, index, field, value) => {
        // console.log("section ===>", section)
        // console.log("index====>", index)
        // console.log("field===>", field)
        // console.log("value====>", value)
        setResumeData(prevData => {
            console.log("prev data====>", prevData)
            const updatedSection = [...prevData[section]];  // Create a copy of array
            updatedSection[index] = {
                ...updatedSection[index],
                [field]: value
            };

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
            [section]: [...prevData[section], {}]  // Add an empty object
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
    const handleSave = async () => {
        try {
            await tempapi.put('/api/save-resume', resumeData);  // Replace with your PUT/PATCH endpoint
            alert('Resume saved successfully!');
        } catch (err) {
            setError(`Failed to save resume: ${err.message}`);
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
                            <td colSpan={5}>
                            <textarea value={exp.responsibilities || ''} onChange={(e) => handleArrayItemChange('experiences', index, 'responsibilities', e.target.value)} />
                            </td>
                        </tr>
                    </tbody>
                    ))}
                </table>

                <div>
                    <button onClick={() => handleAddItem('experiences')}>Add Experience</button>
                </div>
            </section>
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
                                <button onClick={() => handleRemoveItem('skills', index)}>Remove</button>
                            </td>
                        </tr>
                    </tbody>
                    ))}
                </table>
                <button onClick={() => handleAddItem('skills')}>Add Certifications</button>
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
                <button onClick={handleSave}>Save Resume</button>
            </section>


        </div>
    );
}

export default ResumeEditor;
