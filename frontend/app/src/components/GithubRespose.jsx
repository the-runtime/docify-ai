import React from 'react'
import { Card, CardContent, Typography,TextField, Button} from "@mui/material";
// import "./GithubResponse.css"
const GithubResponseCard = ({ githubInfo}) => {
    return (
        <Card>
            <CardContent>
                <div>
                <Typography className="repo-name" variant="h6" gutterBottom>
                    {githubInfo.name}
                </Typography>
                </div>
                <div className="repo-des">
                <p>
                    {githubInfo.desc}
                </p>
                </div>
                <TextField className="url-input" label="Enter working directory" variant="outlined"/>
                <Button className="enter-button" variant="Contained" onClick={GenerateDoc}>Generate Doc</Button>
            </CardContent>
        </Card>
    )
}

function GenerateDoc(name) {
    console.log(name)
}

export default GithubResponseCard