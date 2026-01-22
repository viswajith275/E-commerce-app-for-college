import React,{ useState } from 'react'
import { Text, View, StyleSheet, SafeAreaViewBase, TouchableOpacity, KeyboardAvoidingView, Platform, TextInput, Alert  } from 'react-native'
import { useForm,Controller } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'

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


export default function RegisterScreen({ navigation }){
    const [isLoading, setIsLoading] = useState(false);

    const onRegister = async() =>{

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