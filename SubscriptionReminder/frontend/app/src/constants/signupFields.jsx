const signupFields=[
    {
        labelText:"Username",
        labelFor:"username",
        id:'username',
        name:'username',
        type:'username',
        autoComplete:'username',
        isRequired:true,
        placeholder:"Username"
    },
    {
        labelText:"Email adress",
        labelFor:"email-address",
        id:"email-address",
        name:"email",
        type:"email",
        autoComplete:"email",
        isRequired:true,
        placeholder:"Email address"
    },
    {
        labelText:"Password",
        labelFor:"password",
        id:"password",
        name:"password",
        type:"password",
        autoComplete:"current-password",
        isRequired:true,
        placeholder:"Password"
    },

    {
        labelText:"Confirm Password",
        labelFor: "confirm password",
        id:"confirm password",
        name: "Confirm password",
        type: "confirm password",
        autoComplete:"confirm password",
        isRequired:true,
        placeholder:"Confirm Password"
    }
]

export {signupFields}