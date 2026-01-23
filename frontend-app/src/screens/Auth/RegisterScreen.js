import React,{ useState } from 'react'
import { Text, View, StyleSheet, SafeAreaViewBase, TouchableOpacity, KeyboardAvoidingView, Platform, TextInput, Alert  } from 'react-native'
import { useForm,Controller } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import api from '../../services/api'

//Config
const COLLEGE_DOMAIN = '@gectcr.ac.in'

//Validation
const registerSchema = z.object({
    fullname:z.string().min(2,'Name is too Short'),
    email:z.email('Invalid Email').refine(
        (val) => val.endsWith(COLLEGE_DOMAIN),
        {message:"Must be a GECT Student Email"}
    ),
    phone_no:z.number(),
    password:z.string().min(8,"Password is too Short"),
    confirmPassword:z.string().min(8)
}.refine((data)=>data.password === data.confirmPassword,
    {
        message: "Password do not match",
        path:[confirmPassword]
    }
))

const { control, handleSubmit, formState :{errors}} = useForm({
    resolver: zodResolver(registerSchema)
})


export default function RegisterScreen({ navigation }){
    const [isLoading, setIsLoading] = useState(false);

    const onRegister = async() =>{
        setIsLoading(true);
        try{
            
            api.post("/register",{
                email: data.email,
                password: data.password,
                username: data.fullname,
                phone_no: data.phone_no
            })
            alert.Alert("Registered Successfully")
        }
        catch(error){
            console.log(error);
            alert.Alert("Error.Registering Failed");
        }
        finally{
            setIsLoading(false)
        }
    }

    return(
        <SafeAreaView style={{flex:1,backgroundColor:'#fff'}}>
            <KeyboardAvoidingView
            behavior={Platform.OS == 'ios'? "padding":"height" }
            style={{flex:1}}
            >
            </KeyboardAvoidingView>
        </SafeAreaView>
    )
}