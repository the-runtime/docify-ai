import React, {useEffect, useState} from "react";
import {Navigate} from 'react-router-dom';


const AuthMiddleware =  ({children}) => {
    const [authState, setAuthState] = useState(false)
    const [ranAuthCheck, setAuthCheck] = useState(false)

    useEffect(() => {
        checkAuthentication().then(auth => {
            setAuthState(auth)
            setAuthCheck(true)
        })
    }, [])
    if(!ranAuthCheck) {
        return null
    }

    if (!authState) {
        return <Navigate to="/login"/>
    }

    return children
}

async function checkAuthentication(){
    // const serv_add = import.meta.env.VITE_SERVER_ADDRESS
    try {
        const resp = await fetch(`https://docify.tabish.tech/api/checkauth`, {
            method: 'GET',
            credentials: 'include'
        })
        if (resp.ok) {
            const data = await resp.json()
            console.log(typeof data.is_authenticated)
            return data.is_authenticated
        }
    } catch (error) {
        console.error(error)
        // for web app testing
        return true
    }

}

export default AuthMiddleware