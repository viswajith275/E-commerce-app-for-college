import React,{ useState } from 'react'
import { Text, View, StyleSheet, TouchableOpacity, KeyboardAvoidingView, Platform, TextInput, Alert, ScrollView  } from 'react-native'
import { useForm,Controller } from 'react-hook-form'
import { SafeAreaView } from 'react-native-safe-area-context'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import api from '../../services/api'
// import { useNavigation } from '@react-navigation/native'

//Config
const COLLEGE_DOMAIN = '@gectcr.ac.in'

//Validation
const registerSchema = z.object({
    fullName:z.string().min(2,'Name is too Short'),
    email:z.email('Invalid Email').refine(
        (val) => val.endsWith(COLLEGE_DOMAIN),
        {message:"Must be a GECT Student Email"}
    ),
    phone_no:z.string().min(10,"Invalid Phone Number"),
    password:z.string().min(8,"Password is too Short"),
    confirmPassword:z.string().min(8)
}).refine((data)=>data.password === data.confirmPassword,
    {
        message: "Password do not match",
        path:["confirmPassword"]
    }
)


export default function RegisterScreen({ navigation }){
    const [isLoading, setIsLoading] = useState(false);

    const { control, handleSubmit, formState :{errors}} = useForm({
        resolver: zodResolver(registerSchema)
    })

    const onRegister = async(data) =>{
        setIsLoading(true);
        try{
            
            api.post("/register",{
                email: data.email,
                password: data.password,
                username: data.fullName,
                phone_no: data.phone_no
            })
            Alert.alert("Registered Successfully")
        }
        catch(error){
            console.log(error);
            Alert.alert("Error.Registering Failed");
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
                <ScrollView>
                    <Text>Create an Account</Text>
                    
                    <View>
                        <Text>Username</Text>
                        <Controller
                            control={control}
                            name="fullName"
                            render={({field:{onChange,value}})=>(
                                <TextInput
                                    placeholder='Username'
                                    value={value}
                                    onChangeText={onChange}
                                />
                            )}
                        />
                        <Text>{errors.fullname && <Text>{errors.fullname.message}</Text>}</Text>
                    </View>

                    <View>
                        <Text>E-mail</Text>
                        <Controller
                            control={control}
                            name="email"
                            render={({field:{onChange,value}})=>(
                                <TextInput
                                    placeholder='placeholder@gectcr.ac.in'
                                    value={value}
                                    onChangeText={onChange}
                                />
                            )}
                        />
                        <Text>{errors.email && <Text>{errors.email.message}</Text>}</Text>
                    </View>

                    <View>
                        <Text>Phone Number</Text>
                        <Controller
                            control={control}
                            name="phone_no"
                            render={({field:{onChange,value}})=>(
                                <TextInput
                                    placeholder='9023948576'
                                    value={value}
                                    onChangeText={onChange}
                                />
                            )}
                        />
                        <Text>{errors.phone_no && <Text>{errors.phone_no.message}</Text>}</Text>
                    </View>

                    <View>
                        <Text>Password</Text>
                        <Controller
                            control={control}
                            name="password"
                            render={({field:{onChange,value}})=>(
                                <TextInput
                                    placeholder='Password@123'
                                    value={value}
                                    onChangeText={onChange}
                                />
                            )}
                        />
                        <Text>{errors.password && <Text>{errors.password.message}</Text>}</Text>
                    </View>

                    <View>
                        <Text>Confirm Password</Text>
                        <Controller
                            control={control}
                            name="confirmPassword"
                            render={({field:{onChange,value}})=>(
                                <TextInput
                                    placeholder='Password@123'
                                    value={value}
                                    onChangeText={onChange}
                                />
                            )}
                        />
                        <Text>{errors.confirmPassword && <Text>{errors.confirmPassword.message}</Text>}</Text>
                    </View>
                    
                    <TouchableOpacity
                        onPress={handleSubmit(onRegister)}
                        disabled={isLoading}
                    >
                        <Text>{isLoading? 'Submitting' : 'Register'}</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                        onPress={()=>navigation.navigate("Login")}
                    >
                        <Text>Already have an Account? <Text style={{fontWeight:'bold', color:'#007AFF'}}>Log In</Text></Text>
                    </TouchableOpacity>

                </ScrollView>
            </KeyboardAvoidingView>
        </SafeAreaView>
    )
}