import {createContext, useState, useEffect} from 'react';
import axios from "axios";
import {environment} from "./Enviroment";

export const AuthContext = createContext({
    isAuthenticated: false,
    isLoading: true
});

export const AuthProvider = ({ children } : any) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        setIsLoading(true);
        axios.get(environment + `/whoami`)
            .then(res => {
                if (res.status === 200){
                    setIsAuthenticated(true);
                }
                setIsLoading(false);
            })
            .catch(() => {
                setIsAuthenticated(false);
                setIsLoading(false);
            });
    }, []);


    return (
        <AuthContext.Provider value={{ isAuthenticated, isLoading }}>
            {children}
        </AuthContext.Provider>
    );
};
