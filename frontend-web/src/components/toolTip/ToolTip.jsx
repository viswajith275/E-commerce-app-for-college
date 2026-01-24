import styles from './ToolTip.module.css';

const ToolTip = ({ children, className = "", isVisible = false }) => {
    return (
        <div 
            className={`${styles.toolTip} ${isVisible ? styles.visible : ''} ${className}`}
        >
            {children}
        </div>
    );
}

export default ToolTip;