import React, { useState, useEffect } from "react";
import axios from "axios";

function Sidebar() {
  const [project, setProject] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const token =
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxLCJleHAiOjE2NTE4MzAyMTZ9.l3B1mtfcsVH9VmaCP_RSeSOSNr7HfOaq9cbBLKBgz3o";
      const config = { headers: { Authorization: `Bearer ${token}` } };
      const data = await axios.get("http://localhost:5000/projects", config);

      // TODO update project state here with response
      setProject(data.data);
    };

    fetchData();
  }, []);

  return <h1>Projects</h1>;
}

export default Sidebar;
