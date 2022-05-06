import React from "react";

function Form() {
    
    const [project, setProject] = React.useState(["Project 1", "Project 2"])
    
    function addProject() {
        setProject(prevProject => {
            return [...prevProject, `Project ${prevProject.length +1}`]
        })
    }

    const projectElement = project.map(element => <p key={element}>{element}</p>)

    return (
        <div>
            <button onClick={addProject}>Add Project</button>
            {projectElement}
        </div>
    )}

export default Form 