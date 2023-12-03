import React from 'react';
import {Card, CardContent, List, ListItem, ListItemText, ListItemIcon, Typography} from "@mui/material";
import {Download as DownloadIcon} from "@mui/icons-material";

const DocumentHistoryCard = ({ documentHistory}) => {
   console.log(documentHistory)
    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Document Generation History
                </Typography>
                <List>
                    {documentHistory.map((document, index) => (
                        <ListItem key={index}>
                            <ListItemIcon>
                                <DownloadIcon/>
                            </ListItemIcon>
                            {/*use button to open new window to download the file, rather than opening link in same page*/}
                            <ListItemText primary={document.generationTime} secondary={<a href={`${document.fileDownloadLink}`}>{document.filename}</a> }/>
                        </ListItem>
                    ))}
                </List>
            </CardContent>
        </Card>
    )
}

export default DocumentHistoryCard