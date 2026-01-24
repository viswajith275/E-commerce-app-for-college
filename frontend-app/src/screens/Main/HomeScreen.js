import React,{useContext} from "react";
import { View, Text, Button, StyleSheet } from 'react-native'
import { AuthContext } from "../../context/AuthContext";


export default function HomeScreen (){
    const { logout, user } = useContext(AuthContext);

    return(
        <View style={styles.container}>
            <Text style={styles.text}>Welcome, {user}</Text>
            <Text style={styles.subText}>You are logged in</Text>
            <Button title = 'Logout' onPress={logout}/>
        </View>
    )
}

const styles = StyleSheet.create({
    container:{ flex:1, justifyContent:'center', alignItems:'center'},
    text:{ fontSize:24, fontWeight:'bold'},
    subText:{ color: 'gray', fontSize:16, marginBottom:20 }
})