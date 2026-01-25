import React,{ useContext} from "react";
import { ActivityIndicator, View } from "react-native";
import { NavigationContainer } from '@react-navigation/native'
import { AuthContext } from "../context/AuthContext";
import AppStack from "./AppStack";
import AuthStack from "./AuthStack";

export default function AppNav(){
    const { isLoading, user } = useContext(AuthContext);

    if(isLoading){
        return(
            <View style={{flex:1,justifyContent:'center', alignItems:'center'}}>
                <ActivityIndicator size={"large"}/>
            </View>
        )
    }

    return(
        <NavigationContainer>
            {user !== null ? <AppStack/> : <AuthStack/> }
        </NavigationContainer>
    )
}