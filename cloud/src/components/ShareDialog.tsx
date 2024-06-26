import {Box, FormControl, IconButton, InputLabel, List, MenuItem, Modal, Select, TextField} from "@mui/material";
import {Add} from "@mui/icons-material";
import {UserListItem} from "./UserListItem";
import {useEffect, useState} from "react";
import axios from "axios";
import {environment} from "../utils/Enviroment.tsx";


export const ShareDialog=({open,setIsOpen,boardId})=>{
    const [newEmail, setNewEmail] = useState('');
    const [newRole, setNewRole] = useState('Viewer');
    const [users, setUsers] = useState([]);

    const fetchData = () => {
        axios.get(environment + `/board/${boardId}/privileges`).then(res => {
            if (res.status === 200) {
                setUsers(res.data);
            }
        }).catch((error) => {
            console.log(error)
        });

    }

    useEffect(() => {
        fetchData()
    }, [])

    const handleChangeRole = (e) => {
        setNewRole(e.target.value as string);
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

    const handleShare = () => {
        axios.post(environment + `/boards/share`, {
            board_id: boardId,
            email: newEmail,
            role: newRole
        }).then(res => {
            if (res.status === 200) {
                console.log(res.data)
                fetchData()
            }
        }).catch((error) => {
            console.log(error)

        });
    }

    return <Modal
        open={open}
        onClose={() => setIsOpen(false)}
        aria-labelledby="parent-modal-title"
        aria-describedby="parent-modal-description"
    >
        <Box sx={{...style, width: 400}}>
            <h2 id="parent-modal-title">Shared With</h2>
            <Box display="flex" flexDirection={"row"}>
                <TextField
                    id="new-email"
                    fullWidth
                    label="Email"
                    style={{marginRight:"10px"}}
                    value={newEmail}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                        setNewEmail(event.target.value);
                    }}
                />
                <FormControl style={{width:"250px",marginRight:"10px"}}>
                    <InputLabel id="demo-simple-select-label">Age</InputLabel>
                    <Select
                        value={newRole}
                        label="Role"
                        onChange={handleChangeRole}
                    >
                        <MenuItem value={"Viewer"}>Viewer</MenuItem>
                        <MenuItem value={"Editor"}>Editor</MenuItem>
                        <MenuItem value={"Owner"}>Owner</MenuItem>
                    </Select>
                </FormControl>

                <IconButton onClick={handleShare} style={{width: "50px", height: "50px"}}>
                    <Add fontSize="small"/>
                </IconButton>
            </Box>
            <List style={{maxHeight: '200px', overflow: 'auto'}}>
                {users.map((user)=>
                    <UserListItem key={user.id} role={user.role} email={user.email} id={user.id} fetch={fetchData} boardId={boardId}/>
                )}
            </List>
        </Box>
    </Modal>
}