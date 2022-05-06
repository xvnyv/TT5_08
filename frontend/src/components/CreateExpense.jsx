import React from 'react'

function CreateExpense() {

    const handleClick = () => {

    }

    return (
        <div className='border border-5 border-dark py-4'>
            <form action="">
                <div className='m-2'>
                    <label htmlFor="name">Expense Name </label>
                    <input type="name" />
                </div>
                <div className='m-2'>
                    <label htmlFor="amount">Expense Amount </label>
                    <input type="number" />
                </div>
                <div className='m-2'>
                    <label htmlFor="des">Expense Description </label>
                    <textarea type="des" cols="50"/>
                </div>
                
            </form>

            <div className='text-center'>
            <button onClick={handleClick} className='btn btn-dark'>Create new expense</button>
            </div>
        </div>
    )
}


export default CreateExpense