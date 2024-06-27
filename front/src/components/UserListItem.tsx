import {Box, IconButton, Typography} from "@mui/material";
import {Close, Delete} from "@mui/icons-material";
import axios from "axios";
import {environment} from "../utils/Enviroment.tsx";


export const UserListItem = ({id, email, role, fetch, boardId}) => {

    const handleClick = () => {
        console.log("delete", id, email, role)
        axios.post(environment + `/boards/unshare`, {
            board_id: boardId,
            email: email,
            role: ""
        }).then(res => {
            if (res.status === 200) {
                console.log(res.data)
                fetch()
            }
        }).catch((error) => {
            console.log(error)

        });
    }

    return <Box sx={{ my:1,boxShadow: 2,border:1,borderColor:"gray" ,borderRadius:2, padding:"10px"}}  key={id} display="flex"  flexDirection="row" alignItems="center" justifyContent="space-between">
        <Typography>{email}</Typography>
        <Box display="flex" flexDirection="row" alignItems="center">
            <Typography color="gray">{role}</Typography>
            <IconButton aria-label="Delete" onClick={handleClick}>
                <Close fontSize="small" color="red"/>
            </IconButton>
        </Box>
    </Box>
};