import {Box} from "@mui/material";
import Board from "../components/Board";

export default function SingleBoard(){
    return <Box width="100%"><Board readOnly={false}/></Box>
}