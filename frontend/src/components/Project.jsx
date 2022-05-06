import React, { useContext, useState } from 'react'
import MainContext from '../context/MainContext'


function Project() {
    // const[viewProject,setviewProject,username] = useContext(MainContext);
    const [isEdit, setIsEdit] = useState(false);

    const viewProject = {
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
    }


    const { name, description, amount, created_at, created_by, updated_at, updated_by } = viewProject;

    const handleClickEdit = () => setIsEdit(true);

    const handleSubmit = async(e) => {
        e.preventDefault();

        console.dir(e)
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
                        <div className='text-center'>
                            <h1 >{name}</h1>
                            <p>{description}</p>
                        </div>
                        <div className='mx-5'>
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
                            <button type='Submit'>Submit Changes</button>
                        </div>
                    </div >
                </form>
            )
                :
                (
                    < div >
                        <div className='text-center'>
                            <h1 >{name}</h1>
                            <p>{description}</p>
                        </div>
                        <div className='mx-5'>
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
                            <button className="btn btn-dark"onClick={handleDelete}>Delete Project</button>
                        </div>
                    </div >
                )}


        </div>

    )
}

export default Project