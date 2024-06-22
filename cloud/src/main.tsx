import ReactDOM from 'react-dom/client'
import {createBrowserRouter, Navigate, RouterProvider,} from "react-router-dom"
import './index.css'
import Login from "./pages/Login.tsx";
import {createTheme, ThemeProvider} from "@mui/material";
import axios from "axios";
import SingleBoard from "./pages/SingleBoard";
import Boards from "./pages/Boards";

axios.defaults.withCredentials = true

const theme = createTheme({
    palette: {
        primary: {
            main: "#0f0b0a",
        },
        secondary: {
            main: "#fdefc7",
            contrastText: 'white'
        },
    },
});

const router = createBrowserRouter([
    {path:"/login", element:<Login/>},
    {path:"/board/:id", element:<SingleBoard/>},
    {path:"/boards", element:<Boards/>},
    {path:"*", element: <Navigate to="/boards" replace />},
])


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    //<React.StrictMode>
    <ThemeProvider theme={theme} >
            <RouterProvider router={router}/>
    </ThemeProvider>
    //</React.StrictMode>,
)