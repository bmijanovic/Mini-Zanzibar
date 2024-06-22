import {
    Box,
    Avatar,
    Card,
    CardActions,
    CardContent,
    IconButton, Typography
} from "@mui/material";
import {Add, Delete, Share} from "@mui/icons-material";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {ShareDialog} from "./ShareDialog";
import {DeleteDialog} from "./DeleteDialog";


export default function BoardCard({propBoard}) {
    const [openShareDialog,setIsOpenShareDialog]=useState(false);
    const [openDeleteDialog,setIsOpenDeleteDialog]=useState(false);
    const [board] = useState(propBoard);
    const navigate = useNavigate();

    const handleDeleteClick = (e) => {
        e.stopPropagation(); // Prevent
        setIsOpenDeleteDialog(true);
    };
    const handleShareClick = (e) => {
        e.stopPropagation(); // Prevent
        setIsOpenShareDialog(true);
    };


    return <><Card sx={{maxWidth: 345}} onClick={() => navigate(`/board/${board.id}`)}>
        <CardContent>
            <Box display={"flex"} flexDirection={"row"} justifyContent={"space-between"}>
                <Typography fontSize={25}>{board.name}</Typography>
                <Box display="flex" flexDirection={"row"} justifyContent="center">
                    {board.isOwner &&
                        <IconButton aria-label="Share" onClick={handleShareClick}>
                            <Share fontSize="small"/>
                        </IconButton>
                    }
                    {board.isOwner &&
                        <IconButton aria-label="Delete" onClick={handleDeleteClick}>
                            <Delete fontSize="small" color="red"/>
                        </IconButton>
                    }

                </Box>
            </Box>

        </CardContent>
        <CardActions disableSpacing>
            <Box display="flex" width="100%" justifyContent={"space-between"}>

                <Box display={"flex"} flexDirection={"row"} alignItems="center" justifyContent={"center"}>
                    <Typography fontSize={12} fontWeight={400}>{board.role}</Typography>
                </Box>
                <Box display={"flex"} flexDirection={"row"} alignItems="center" justifyContent={"center"}>
                    <Typography fontSize={12} fontWeight={200} marginRight={1}>Created by</Typography>
                    <Typography fontWeight={600}>{board.owner}</Typography></Box>
            </Box>
        </CardActions>
    </Card>
        <ShareDialog open={openShareDialog} setIsOpen={setIsOpenShareDialog}/>
        <DeleteDialog open={openDeleteDialog} setIsOpen={setIsOpenDeleteDialog}/>
    </>
}