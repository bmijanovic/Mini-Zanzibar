import {useContext} from "react";
import {Navigate} from "react-router-dom";
import {AuthContext} from "../utils/AuthContext";

export const UnauthenticatedRoute = ({ children } : any) => {
    const { isAuthenticated, isLoading } = useContext(AuthContext);
    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (isAuthenticated) {
        return <Navigate to="/boards" />;
    }

    return children;
};