import {Avatar, Box, Card, CardActions, CardContent, CardHeader, Collapse, IconButton, Typography} from "@mui/material";


export default function BoardCard(){
    return <Card sx={{ maxWidth: 345 }}>
        <CardHeader
            action={
                <IconButton aria-label="settings">
                </IconButton>
            }
            title="Shrimp and Chorizo Paella"
            subheader="September 14, 2016"
        />
        <CardContent>
            <Typography variant="body2" color="text.secondary">
                This impressive paella is a perfect party dish and a fun meal to cook
                together with your guests. Add 1 cup of frozen peas along with the mussels,
                if you like.
            </Typography>
        </CardContent>
        <CardActions disableSpacing>
        </CardActions>
    </Card>
}