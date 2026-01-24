import styles from './Switch.module.css';

const Switch = ({className = "", size = 16}) => {
    const width = size * 2;

    return (
        <label className={`${styles.switch} ${className}`}>
            <input type="checkbox" style={{ width: width, height: size }}/>
        </label>
    );
}

export default Switch;