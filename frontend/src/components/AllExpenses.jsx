import React, { useRef, useEffect, useState, useContext } from "react";
import Project from "./Project";
import MainContext from "../context/MainContext";
import CreateExpense from "./CreateExpense";
import axios from "axios";

function AllExpenses() {
  //   const { token } = useContext(MainContext);
  const [expenses, setExpenses] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const project_id = window.location.pathname.split("/")[2];
      const token =
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxLCJleHAiOjE2NTE4MzIwNDV9.MKIG-n4oYUsOwTPME5A6tanm5LOrrSllVrjd54-t6UI";
      const config = { headers: { Authorization: `Bearer ${token}` } };
      const data = await axios.get(
        `http://localhost:5000/expense/${project_id}`,
        config
      );

      // TODO update project state here with response
      setExpenses(data.data);
    };
    fetchData();
  }, []);

  const viewProject = [
    {
      id: 1,
      project_id: 2,
      category_id: 2,
      name: "Server Maintenance",
      description:
        "Server maintenance and upgrading work to incorporate BC plans",
      amount: 30000,
      created_at: "2021-11-04T16:00:00.000Z",
      created_by: "Jacky",
      updated_at: "2021-11-06T16:00:00.000Z",
      updated_by: "Jacky",
    },
    {
      id: 2,
      project_id: 3,
      category_id: 4,
      name: "Consultant",
      description: "Consultancy services for integration work",
      amount: 10000,
      created_at: "2021-11-06T16:00:00.000Z",
      created_by: "Helen",
      updated_at: "2021-11-07T16:00:00.000Z",
      updated_by: "Helen",
    },
  ];

  return (
    <div>
      {expenses.map((expense, key) => (
        <div className="my-3" key={key}>
          <Project exp={expense} />
        </div>
      ))}
      <CreateExpense />
    </div>
  );
}

export default AllExpenses;
