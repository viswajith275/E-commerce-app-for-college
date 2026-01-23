import styles from './ButtonNB.module.css';

const ButtonNB = ({ children, color = "orange" }) => {
    return (
        <button className={styles.btn} style={{ backgroundColor: color }}>
            {children}
        </button>
    );
}

export default ButtonNB;