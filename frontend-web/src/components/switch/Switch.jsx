import styles from './Switch.module.css';

const Switch = ({color = "white", className = "", size = 16}) => {
    const width = size * 2;

    return (
        <label className={`${styles.switch} ${className}`} style={{ backgroundColor: color }}>
            <input type="checkbox" style={{ width: width, height: size }}/>
        </label>
    );
}

export default Switch;