import React, {useEffect, useState} from "react";
import DocumentHistoryCard from "../components/HistoryCard";
import Basepage from "../pages/Basepage";
import {daDK} from "@mui/material/locale";

function History() {
    const [histories, setHistories] = useState()
   useEffect(() => {
       fetchHistoryInfo().then(data => {
           setHistories(data.history)
           console.log(data)
       })
   }, [])
    if (!histories){
        return null
    }

    return (
        <div className="dashboard-container">
            <DocumentHistoryCard documentHistory={histories}/>
        </div>
    )
}


const fetchHistoryInfo = async () => {
    // const serv_add = import.meta.env.VITE_SERVER_ADDRESS
    try {
        const resp = await fetch(`https://docify.tabish.tech/api/history`, {
            method: 'Get',
            credentials: 'include'
        })

        if (resp.ok) {
            return await resp.json()
        }
    } catch (error) {
        console.log(error)
    }
}

const HistoryPage = (() => {
    return (
        <Basepage name="History">
            <History />
        </Basepage>
    )
})

export default HistoryPage