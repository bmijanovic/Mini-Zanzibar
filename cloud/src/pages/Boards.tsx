import {Box, Fab, Grid, Tab, Typography} from "@mui/material";
import {TabContext, TabList, TabPanel} from '@mui/lab';
import BoardCard from "../components/BoardCard";
import {useState} from 'react'
import {Add, Logout} from "@mui/icons-material";
import {NewBoardDialog} from "../components/NewBoardDialog";
import {useNavigate} from "react-router-dom";
import axios from "axios";
import {environment} from "../utils/Enviroment";

export default function Boards(){
    const [tabValue, setTabValue] = useState('1');
    const [isOpenDialog,setIsOpenDialog]=useState(false);
    const [myBoards, setMyBoards] = useState([{id:3,name:"Board 1",owner:"Vukasin",role:"Owner","isOwner":true},{id:4,name:"Board 1",role:"Owner",owner:"Vukasin","isOwner":true}]);
    const [sharedBoards, setSharedBoards] = useState([{id:1,name:"Board 12",owner:"Vukasin",role:"View Only","isOwner":false},{id:2,name:"Board 12",role:"View Only",owner:"Vukasin","isOwner":false}]);
    const [error, setError] = useState("")
    const navigate = useNavigate()

    const handleChange = (event: React.SyntheticEvent, newValue: string) => {
        setTabValue(newValue);
    };

    function submitHandler(event: any) {
        event.preventDefault()
        axios.post(environment + `/users/logout`).then(res => {
            if (res.status === 200) {
                navigate("/login")
            }
        }).catch((error) => {
            console.log(error)
            setError("An error occurred!");
        });
    }

    return <Box>
        <NewBoardDialog open={isOpenDialog} setIsOpen={setIsOpenDialog}/>
        <Fab size="small" sx={{position:"fixed",right:10,top:10, backgroundColor:"gray"}} aria-label="add">
            <Logout onClick={submitHandler}/>
        </Fab>
        <Fab size="small" variant='extended' sx={{position:"fixed",right:40,bottom:40, backgroundColor:"blue", '&:hover': {
                backgroundColor: "darkblue"
            }}} aria-label="add" onClick={()=>setIsOpenDialog(true)}>
            <Add sx={{color:"white"}}/>
            <Typography color="white">Add New Board</Typography>
        </Fab>
        <Box display="flex" justifyContent="center"><h1>Boards</h1></Box>

        <Box sx={{ width: '100%', typography: 'body1' }}>
            <TabContext value={tabValue}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider' }} display={"flex"} justifyContent="center">
                    <TabList onChange={handleChange} aria-label="lab API tabs example">
                        <Tab label="My" value="1" />
                        <Tab label="Shared" value="2" />
                    </TabList>
                </Box>
                <TabPanel value="1">
                    <Grid container spacing={2}>
                        { myBoards.map((board)=>
                        <Grid key={board.id} item xs={4}>
                            <BoardCard propBoard={board}/>
                        </Grid>
                        )}
                    </Grid>
                </TabPanel>
                <TabPanel value="2">
                    <Grid container spacing={2}>
                        { sharedBoards.map((board)=>
                            <Grid key={board.id} item xs={4}>
                                <BoardCard propBoard={board}/>
                            </Grid>
                        )}
                    </Grid>
                </TabPanel>
            </TabContext>
        </Box>


    </Box>
}