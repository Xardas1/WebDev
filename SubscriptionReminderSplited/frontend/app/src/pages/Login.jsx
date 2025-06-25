// src/pages/Login.jsx

import Header from '../components/Header';
import Login from '../components/Login'; // ✅ this is your new Login form component

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="flex flex-col items-center justify-center">
    <Header
        heading="Login to your account"
        paragraph="Don't have an account yet?"
        linkName="Signup"
        linkUrl='/signup'
    />
    <Login/>
    </div>
    </div>
);
}
