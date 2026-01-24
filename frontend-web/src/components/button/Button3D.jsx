import styles from './Button.module.css';

const Button3D = ({ children, color = "white" }) => {
    return (
        <button className={styles.btn3D} style={{ backgroundColor: color }}>
            {children}
        </button>
    );
}

export default Button3D;