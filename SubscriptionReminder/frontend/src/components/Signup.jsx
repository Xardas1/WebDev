import { useState } from 'react';
import { signupFields } from "../constants/signupFields"
import Input from "./Input";
import api from "../api";
import { useAuth } from "../context/AuthContext";

const fields = signupFields;
let fieldsState = {};

fields.forEach(field => fieldsState[field.name] = '');

export default function Login() { 
    const [loginState, setLoginState] = useState(fieldsState);

    const handleChange = (e) => {
        setLoginState({ ...loginState, [e.target.name]: e.target.value});
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await api.post('/register', {
                username: loginState.username,
                email: loginState.email,
                password: loginState.password
            });

            console.log("✅ Registered:", response.data);

            // Optional: Log them in right away
            const params = new URLSearchParams();
            params.append('username', loginState.email);
            params.append('password', loginState.password);

            const loginResponse = await api.post('/token', params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });

            // Use the context login method (if you use AuthContext)



        } catch (error) {
            console.error("❌ Signup failed:", error);
            alert("Signup failed. Try again or use a different email.");
        }
    };







    return (
        <form className="space-y-6" onSubmit={handleSubmit}>
        {fields.map(field => (
            <Input
            key={field.id}
            handleChange={handleChange}
            value={loginState[field.name]}
            name={field.name}
            type={field.type}
            id={field.id}
            labelText={field.labelText}
            labelFor={field.labelFor}
            isRequired={field.isRequired}
            placeholder={field.placeholder}
            customClass="mb-4 text-black border-neutral-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            />
        ))}

            <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-gray-800 bg-ascent focus:outline-none focus:ring-2 focus:ring-offset-2 hover:bg-gray-700"
            >
                Sign up
            </button>
        </form>
    );
}