import React from "react"
import {AppBar, Container, CssBaseline, Paper, Toolbar, Typography} from "@mui/material";
import {Link} from "react-router-dom";
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
            <AppBar position="sticky">
                <Toolbar>
                    <Typography variant='h6' sx={{ marginRight: 100 }} > Docify-ai</Typography>
                    {/*we can use alert to give alert if a user is trying to access with login*/}
                    <Typography variant='h6' sx={{marginRight: 10}}> <Link to="/dashboard" style={linkStyle}>Dashboard</Link></Typography>
                    <Typography variant='h6' sx={{marginRight: 10}}> <Link to="/documents" style={linkStyle}>Documents</Link></Typography>
                    <Typography variant='h6' > <Link to="/settings"  style={linkStyle}>Settings</Link></Typography>
                </Toolbar>
            </AppBar>
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