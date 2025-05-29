import {Link} from 'react-router-dom';
import logo from '../images/logo.png';

export default function Header({
    heading,
    paragraph,
    linkName,
    linkUrl="#"
}) {
return(
    <div className="mb-5">
        <div className="flex items-center justify-center">
        <img
            src={logo}
            alt="App logo"
            className="h-20 w-20"
        />
    </div>
    <h2 className=" text-center text-3xl font-extrabold text-white">
            {heading}
        </h2>
        <p className="text-center text-sm text-gray-400 mt-4"> 
            {paragraph} {' '}
            <Link to={linkUrl} className="font-medium text-indigo-500 hover:text-black-500">
                {linkName}
            </Link>
        </p>
    </div>
);
}