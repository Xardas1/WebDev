import Header from "../components/Header";
import Signup from "../components/Signup";

export default function SignupPage() {
    return(
        <>
        <div className="min-h-screen flex items-center justify-center">
            <div>
            <Header
            heading="Signup to create an account"
            paragraph="Already have an account?"
            linkName="Login"
            linkUrl="/login"
            />
            <Signup/>
        </div>
    </div>
   </>
    );
}