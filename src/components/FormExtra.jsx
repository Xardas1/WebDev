import { Link } from "react-router-dom";


export default function FormExtra() {
    return (
        <div className="w-full flex items-center justify-between text-sm">
            <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
                />
            <label htmlFor="remember-me" className="ml-1 text-emerald-500 hover:text-amber-500">
               Remember me
            </label>
            </div>
            <div>
                <Link to="/forgot-password" className="text-emerald-500 hover:text-amber-500">
                    Forgot your password?
                </Link>
            </div>
        </div>
    );
}