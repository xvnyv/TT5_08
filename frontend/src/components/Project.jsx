import React, { useContext, useState,useRef } from 'react'
import MainContext from '../context/MainContext'


function Project(props) {
    // const[viewProject,setviewProject,username] = useContext(MainContext);
    const username = "test-user"
    const budgetRef = useRef();
    const nameRef = useRef();
    const desRef = useRef();
    const [isEdit, setIsEdit] = useState(false);

    const viewProject = props.exp;

    const { name, description, amount, created_at, created_by, updated_at, updated_by } = viewProject;

    const handleClickEdit = () => setIsEdit(true);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const req = {
            name : nameRef.current.value,
            description : desRef.current.value,
            amount: Number(budgetRef.current.value),

        }
        console.log(req)
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
                        <h1><input ref={nameRef} type="text" id="name" placeholder={name} /></h1>
                            <p><textarea ref={desRef} cols="100" type="text" id="description" placeholder={description} /></p>
                        </div>
                        
                        <div className='py-3 px-1 my-2 mx-5 border border-dark border-2 rounded'>
                            <p>
                                <label htmlFor="Budget">Expense amount: </label>
                                <input ref={budgetRef} type="text" id="Budget" placeholder={amount} />
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
                        <div className='py-3 px-1 my-2 mx-5 border border-dark border-2 rounded'>
                            <p>
                                Expense amount: {amount}
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


