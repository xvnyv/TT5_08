import React, { useContext, useState } from 'react'
import MainContext from '../context/MainContext'


function Project() {
    // const[viewProject,setviewProject,username] = useContext(MainContext);
    const username = "test-user"

    const [isEdit, setIsEdit] = useState(false);
    
    const viewProject = [{
        "id": 1,
        "project_id": 2,
        "category_id": 2,
        "name": "Server Maintenance",
        "description": "Server maintenance and upgrading work to incorporate BC plans",
        "amount": 30000,
        "created_at": "2021-11-04T16:00:00.000Z",
        "created_by": "Jacky",
        "updated_at": "2021-11-06T16:00:00.000Z",
        "updated_by": "Jacky"
    }]


    const { name, description, amount, created_at, created_by, updated_at, updated_by } = viewProject;

    const handleClickEdit = () => setIsEdit(true);

    const handleSubmit = async(e) => {
        e.preventDefault();
        viewProject.updated_at = Date()
        viewProject.updated_by = username ;
        console.dir(e)
        console.log(viewProject)
        // TODO - submit to server
    }

    const handleDelete = async () => {
        // Navigate to projects homepage
        // Delete from server
        // Need to set projects in context
    }


    return (
        <div>
            {isEdit ? (
                <form onSubmit={handleSubmit}>
                    < div >
                        <div className='text-center bg-secondary rounded-pill py-3'>
                            <h1 >{name}</h1>
                            <p>{description}</p>
                        </div>
                        {viewProject.map((expense,key)=>()}
                        
                        <div className='py-3 px-1 my-2 mx-5 border border-dark border-5 rounded'>
                            <p>
                                <label htmlFor="Budget">Budget: </label>
                                <input type="text" id="Budget" placeholder={amount} />
                            </p>
                            <p>
                                Expense Created on: {created_at}
                            </p>
                            <p>
                                Expense Created by: {created_by}
                            </p>
                            <p>
                                Expense Last Updated on: {updated_at}
                            </p>
                            <p>
                                Expense Last Updated by: {updated_by}
                            </p>
                        </div>
                        <div className='text-center'>
                            <button className="btn btn-dark" type='Submit'>Submit Changes</button>
                        </div>
                    </div >
                </form>
            )
                :
                (
                    < div >
                        <div className='text-center bg-secondary rounded-pill py-3'>
                            <h1 className=''>{name}</h1>
                            <p className='text-faded'>{description}</p>
                        </div>
                        <div className='py-3 px-1 my-2 mx-5 border border-dark border-5 rounded'>
                            <p>
                                Budget: {amount}
                            </p>
                            <p>
                                Expense Created on: {created_at}
                            </p>
                            <p>
                                Expense Created by: {created_by}
                            </p>
                            <p>
                                Expense Last Updated on: {updated_at}
                            </p>
                            <p>
                                Expense Last Updated by: {updated_by}
                            </p>
                        </div>
                        <div className='text-center'>
                            <button className="btn btn-dark me-2" onClick={handleClickEdit}>Edit</button>
                            <button className="btn btn-dark" onClick={handleDelete}>Delete Project</button>
                        </div>
                    </div >
                )}


        </div>

    )
}

export default Project