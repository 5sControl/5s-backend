import { Algorithm, Camera, Dashboard } from '../assets/svg/SVGcomponent'
import logo from '../assets/svg/icon.svg'

export const LeftMenu = () =>{
    return(
    <aside className="leftMenu">
        <img src={logo} alt='logo'/>
        <ul>
            <li className='active'>
                <Dashboard />
                <span>Dashboard</span>
            </li>
            <li className='noActive'> 
                <Camera/>
                <span>Camera</span>
            </li>
            <li className='noActive'>
                <Algorithm/>
                <span>Algorithm</span>
            </li>
        </ul>
    </aside>
    )
}