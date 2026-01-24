import { useState } from 'react';
import styles from './ToolTip.module.css';

const ToolTipContainer = ({ children, className = "" }) => {
    const [isVisible, setIsVisible] = useState(false);

    const handleMouseEnter = () => setIsVisible(true);
    const handleMouseLeave = () => setIsVisible(false);

    const childContent = typeof children === 'function' 
        ? children(isVisible) 
        : Array.isArray(children)
            ? children.map((child) => 
                child && child.type?.name === 'ToolTip' 
                    ? { ...child, props: { ...child.props, isVisible } }
                    : child
              )
            : children && children.type?.name === 'ToolTip'
                ? { ...children, props: { ...children.props, isVisible } }
                : children;

    return (
        <div 
            className={`${styles.container} ${className}`}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
        >
            {childContent}
        </div>
    );
}

export default ToolTipContainer;