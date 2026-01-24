import React, { createContext, useState, useEffect} from "react";
import api from "../services/api";


export const AuthContext = createContext();

export const AuthProvider = ({ children }) =>{
    [isLoading, setIsLoading] = useState(false);
    [user, setUser] = useState(null);

    const checkLoggedIn = async()=>{

        setIsLoading(true);
        try{
            const response = await api.get("/username");
            setUser(response.data)
        }
        catch(error){
            console.log("Not Logged in");
            setUser(null);
        }
        finally{
            setIsLoading(false);
        }
    }

    //Calls Once during App Startup
    useEffect(()=>{
        checkLoggedIn();
    },[])

    const login = async(user_name,password) =>{
        setIsLoading(true);

        try{

            const formData = new URLSearchParams();

            formData.append("username",user_name);
            formData.append("password",password);
            
            await api.post("/login",formData.toString(),{
                headers : { 'Content-Type' : 'application/x-www-form-urlencoded'}
            })
            
            await checkLoggedIn();
        }
        catch(error){
            console.log("Login Failed ",error);
            alert("Invalid Credentials");
            setIsLoading(false);
        }
    }

    const logout = async()=>{
        setIsLoading(true);
        try{
            await api.post("/logout");
            console.log("Logged Out Successfully");
            setUser(null);
        }
        catch(error){
            console.log(error);
            //Force Logout
            setUser(null);
        }
        finally{
            setIsLoading(false);
        }
    }
    

    return(
        <AuthContext.Provider value={{login, logout, isLoading, user}}>
            { children }
        </AuthContext.Provider>
    )
}