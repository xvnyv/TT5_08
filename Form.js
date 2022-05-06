import React from "react";

function Form() {

    const [project, setProject] = React.useState(
        {projectName: ""}
    )

    function handleChange(event) {
        setProject(prevProject => {
            return {
                ...prevProject,
                [event.target.name]: event.target.value

            }
        })
    }


    return (
        <form>
            <input 
                type="text"
                placeholder="Project Name"
                onChange={handleChange}
                value = {project.projectName}
                name="projectName"
            />
            <button>Submit</button>
        </form>
    )
}

export default Form;