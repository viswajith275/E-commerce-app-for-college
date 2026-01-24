import React, { useContext, useState } from "react";
import { View, Text, TextInput, StyleSheet, Alert, TouchableOpacity, KeyboardAvoidingView, Platform } from 'react-native';
import { AuthContext } from "../../context/AuthContext";
import { SafeAreaView } from "react-native-safe-area-context";
import RegisterScreen from "./RegisterScreen";




export default function LoginScreen({ navigation }){
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');


    const { login, isLoading } = useContext(AuthContext);

    const handleLogin=async()=>{

        if(!username || !password){
            alert.Alert("Both fields need to be filled")
            return;
        }
        
        await login(username,password);
    }

    return(
        <SafeAreaView style={{flex:1,justifyContent:'center',alignItems:'center'}}>
            <KeyboardAvoidingView behavior ={Platform.OS == 'ios'? 'padding':'height'}>
                <View>
                    <Text>Welcome</Text>
                    <Text>Log in to continue</Text>
                    
                    <View>
                        <Text>Email</Text>
                        <TextInput
                            placeholder='Username'
                            value={username}
                            onChange={setUsername}
                        />
                    </View>

                    <View>
                        <Text>Password</Text>
                        <TextInput
                            placeholder='Password'
                            value={password}
                            onChange={setPassword}
                        />
                    </View>
                    <TouchableOpacity onPress={handleLogin} disabled={isLoading}>
                        <Text>{isLoading? 'Logging In': 'Log In'}</Text>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={()=>navigation.navigate(RegisterScreen)}>
                        <Text>Don't have an account? <Text style={{fontWeight:'bold', color:'#007AFF'}}>Sign Up</Text></Text>
                    </TouchableOpacity>
                </View>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );
}