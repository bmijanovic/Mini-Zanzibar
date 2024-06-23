import {Box, Fab, Grid, Tab, Typography} from "@mui/material";
import {TabContext, TabList, TabPanel} from '@mui/lab';
import BoardCard from "../components/BoardCard";
import {useEffect, useState} from 'react'
import {Add, Logout} from "@mui/icons-material";
import {NewBoardDialog} from "../components/NewBoardDialog";
import {useNavigate} from "react-router-dom";
import axios from "axios";
import {environment} from "../utils/Enviroment";

export default function Boards(){
    const [tabValue, setTabValue] = useState('1');
    const [isOpenDialog,setIsOpenDialog]=useState(false);
    const [myBoards, setMyBoards] = useState([]);
    const [sharedBoards, setSharedBoards] = useState([]);
    const [error, setError] = useState("")
    const navigate = useNavigate()
    const handleChange = (event: React.SyntheticEvent, newValue: string) => {
        setTabValue(newValue);
    };

    const fetchData=()=>{
        axios.get(environment + `/boards`).then(res => {
            if (res.status === 200) {
                let myBoards = res.data.my_boards;
                let sharedBoards = res.data.shared_boards;
                setMyBoards(myBoards);
                setSharedBoards(sharedBoards);

            }
        }).catch((error) => {
            console.log(error)
            setError("An error occurred!");
        });
    }

    useEffect(() => {
        fetchData()
    }, [])

    function submitHandler(event: any) {
        event.preventDefault()
        axios.post(environment + `/users/logout`).then(res => {
            if (res.status === 200) {
                navigate(0)
            }
        }).catch((error) => {
            console.log(error)
            setError("An error occurred!");
        });
    }

    return <Box>
        <NewBoardDialog open={isOpenDialog} setIsOpen={setIsOpenDialog} getBoards={fetchData}/>
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
                            <BoardCard propBoard={board} fetchData={fetchData}/>
                        </Grid>
                        )}
                    </Grid>
                </TabPanel>
                <TabPanel value="2">
                    <Grid container spacing={2}>
                        { sharedBoards.map((board)=>
                            <Grid key={board.id} item xs={4}>
                                <BoardCard propBoard={board} fetchData={fetchData}/>
                            </Grid>
                        )}
                    </Grid>
                </TabPanel>
            </TabContext>
        </Box>


    </Box>
}