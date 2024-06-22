import {Box, IconButton, Typography} from "@mui/material";
import {Close, Delete} from "@mui/icons-material";


export const UserListItem = ({id, email, role}) => {
    return <Box sx={{ my:1,boxShadow: 2,border:1,borderColor:"gray" ,borderRadius:2, padding:"10px"}}  key={id} display="flex"  flexDirection="row" alignItems="center" justifyContent="space-between">
        <Typography>{email}</Typography>
        <Box display="flex" flexDirection="row" alignItems="center">
            <Typography color="gray">{role}</Typography>
            <IconButton aria-label="Delete">
                <Close fontSize="small" color="red"/>
            </IconButton>
        </Box>
    </Box>
};