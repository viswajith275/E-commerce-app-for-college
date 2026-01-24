import styles from './Button.module.css';

const Button2D = ({ children, color = "white" }) => {
    return (
        <button className={styles.btn2D} style={{ backgroundColor: color }}>
            {children}
        </button>
    );
}

export default Button2D;