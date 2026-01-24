import React,{ useContext} from "react";
import { ActivityIndicator, View } from "react-native";
import { NavigationConatainer } from '@react-navigation/native'
import { AuthContext } from "../context/AuthContext";
import { AppStack } from "./AppStack";

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
        <NavigationConatainer>
            {user !== null ? <AppStack/> : <AuthStack/> }
        </NavigationConatainer>
    )
}