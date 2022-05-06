import React from "react";

function Sidebar() {
    
    const [project, setProject] = React.useState([])

    useEffect(() => {

        // declare the data fetching function
        
        const fetchData = async () => {
        
        const token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoxLCJleHAiOjE2NTE4MzAyMTZ9.l3B1mtfcsVH9VmaCP_RSeSOSNr7HfOaq9cbBLKBgz3o";
        
        const config = {headers: {Authorization: `Bearer ${token}`}}
        
        const data = await axios.get("http://localhost:5000/projects", config);
        
        // TODO update project state here with response
        
        };
        
        
        
        // call the function
        
        fetchData()
        
        // make sure to catch any error
        
        .catch(console.error);
        
        }, []);


    



    return ()
}

export default Sidebar
