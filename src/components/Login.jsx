import React, { useState } from 'react';
import { loginFields } from '../constants/formFields';
import Input from '../components/Input';
import FormExtra from './FormExtra';

const fields = loginFields;
let fieldsState = {};

fields.forEach(field => fieldsState[field.name] = '');

export default function Login() { 
    const [loginState, setLoginState] = useState(fieldsState);

    const handleChange = (e) => {
        setLoginState({ ...loginState, [e.target.name]: e.target.value});
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Login submitted:", loginState);
        // you can later call API here
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
            customClass="mb-4"
            />
        ))}

        <FormExtra />
        

            <button
                type="submit"
                className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-amber-500 bg-ascent focus:outline-none focus:ring-2 focus:ring-offset-2"
            >
                Sign in
            </button>
        </form>
    );
}