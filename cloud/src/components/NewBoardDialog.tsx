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


export const NewBoardDialog=({open,setIsOpen})=>{
    const [newName, setNewName] = useState('');

    const handleChangeRole = (e) => {
        setNewName(e.target.value as string);
    }
    const style = {
        position: 'absolute' as 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 800,
        bgcolor: 'background.paper',
        boxShadow: 24,
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
            <h2 align="center" id="parent-modal-title">Add new board</h2>
            <Box display="flex" flexDirection={"column"} justifyContent="center" alignItems="center">
                <TextField
                    id="new-board-name"
                    fullWidth
                    label="Board name"
                    style={{marginRight:"10px"}}
                    value={newName}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                        setNewName(event.target.value);
                    }}
                />
                <Button sx={{padding:"10px",bgcolor:"blue",color:"white",'&:hover':{backgroundColor:"darkBlue"} ,fontSize:"15px",fontWeight:"600",width:"200px",mt:4,}} >Create table</Button>
            </Box>

        </Box>
    </Modal>
}