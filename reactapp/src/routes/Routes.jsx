import { LeftMenu } from "../components/leftMenu"
import { Outlet} from 'react-router-dom';

export const RoutesOutlet = () => {
    return (
        <div className="window">        
            <LeftMenu/>
            <sectin className='outlet'>
                <Outlet />
            </sectin>
        </div>
      );
}