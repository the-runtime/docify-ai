import React from "react"
import { Container, CssBaseline, Paper, Toolbar, Typography} from "@mui/material";
import {Link} from "react-router-dom";
import ResponsiveAppBar from "../components/AppBar"
import "./Basepage.css"
 function Basepage({children, name}) {
     const linkStyle = {
         color: 'white',
         underline: 'none',
         textDecoration: 'none',
     };
    return (
        <div className="base-container">
            {/*<CssBaseline/>*/}
            <ResponsiveAppBar />
            
            <Container className="base-content">
                <Paper elevation={3} className="card">
                    <h2>
                        {name}
                    </h2>
                    {children}
                </Paper>
            </Container>
        </div>
    )
}

export default Basepage