import {Link} from 'react-router-dom';
import { CalendarClock } from 'lucide-react';

export default function Header({
    heading,
    paragraph,
    linkName,
    linkUrl="#"
}) {
return(
    <div className="mb-5">
        <div className="flex items-center justify-center">
            <CalendarClock className="w-18 h-18 text-gray-800"/>
        </div>
    <h2 className="text-center text-3xl font-extrabold text-gray-800">
            {heading}
        </h2>
        <p className="text-center text-sm text-gray-800 mt-4"> 
            {paragraph} {' '}
            <Link to={linkUrl} className="font-medium text-indigo-500 hover:text-black-500">
                {linkName}
            </Link>
        </p>
    </div>
);
}