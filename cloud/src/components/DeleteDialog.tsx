import {
    Box,
    Button,
    FormControl,
    IconButton,
    InputLabel,
    List,
    MenuItem,
    Modal,
    Select,
    TextField
} from "@mui/material";
import {Add} from "@mui/icons-material";
import {UserListItem} from "./UserListItem";
import {useState} from "react";


export const DeleteDialog=({open,setIsOpen})=>{
    const style = {
        position: 'absolute' as 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 800,
        bgcolor: 'background.paper',
        boxShadow: 24,
        display:"flex",
        justifyContent:"center",
        flexDirection:"column",
        pt: 2,
        px: 4,
        pb: 3,
    };


    return <Modal
        open={open}
        onClose={() => setIsOpen(false)}
        aria-labelledby="parent-modal-title"
        aria-describedby="parent-modal-description"
    >
        <Box sx={{...style, width: 400}}>
            <Box display={"flex"} textAlign="center" justifyContent={"center"} flexDirection={"column"}>
            <h3 id="parent-modal-title">Are you sure you want to delete board?</h3>
            <Box display="flex" flexDirection={"row"} justifyContent={"space-around"}>
                <Button sx={{backgroundColor:"red",color:"white",paddingX:"30px"}} onClick={()=>setIsOpen(false)} >Yes</Button>
                <Button sx={{borderColor:"gray",border:1,paddingX:"30px"}}  onClick={()=>setIsOpen(false)}>No</Button>
            </Box>
            </Box>

        </Box>
    </Modal>
}