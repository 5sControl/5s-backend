import { LeftMenu } from "../components/leftMenu"
import { Outlet} from 'react-router-dom';

export const RoutesOutlet = () => {
    return (
        <>        
            <LeftMenu/>
            <Outlet />
        </>
      );
}