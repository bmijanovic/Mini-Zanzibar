import {useLayoutEffect, useState} from "react";
import {Avatar, Box, Button, Container, CssBaseline, InputLabel, TextField, Typography} from "@mui/material";
import {useNavigate} from "react-router-dom";
import axios from "axios";
import {environment} from "../utils/Enviroment"

export default function LoginForm() {
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [error, setError] = useState("")
    const navigate = useNavigate()


    function submitHandler(event: any) {
        event.preventDefault()
        axios.post(environment + `/users/login`, {
            email: email,
            password: password
        }).then(res => {
            if (res.status === 200) {
                navigate("/boards")
            }
        }).catch((error) => {
            console.log(error)
            if (error.response?.status !== undefined && error.response.status === 404) {
                setError("Invalid username or password!");
            } else if (error.response?.status !== undefined && error.response.status === 400) {
                setError("Invalid input!");
            } else {
                setError("An error occurred!");
            }
        });
    }

    return <>
        <Container component="main" maxWidth="xs" sx={{backgroundColor:"transparent"}}>
            <CssBaseline/>
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Avatar sx={{m: 1, bgcolor: "#0f0b0a"}}/>

                <Typography component="h1" variant="h3">
                    Sign in
                </Typography>
                <Box component="form" onSubmit={submitHandler} sx={{mt: 1}}>
                    <TextField sx={{backgroundColor:"white"}}
                               margin="normal"
                               required
                               fullWidth
                               autoFocus
                               type="text"
                               id="email"
                               label="Email Address"
                               name="email"
                               autoComplete="email"
                               variant="outlined"
                               onChange={(e) => {
                                   setEmail(e.target.value)
                               }}
                    />
                    <TextField sx={{backgroundColor:"white"}}
                               margin="normal"
                               required
                               fullWidth
                               name="password"
                               label="Password"
                               type="password"
                               id="password"
                               autoComplete="current-password"
                               variant="outlined"
                               onChange={(e) => {
                                   setPassword(e.target.value)
                               }}
                    />
                    <div>
                        <InputLabel style={{color: "red"}}>{error}</InputLabel>
                    </div>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{mt: 3, mb: 3,backgroundColor: "#0f0b0a"}}
                    >
                        Sign In
                    </Button>
                </Box>
            </Box>
        </Container>
    </>
}