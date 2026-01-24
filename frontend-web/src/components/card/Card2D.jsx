import styles from './Card.module.css';

const Card2D = ({ children, color = "white", display = "block", className = "" }) => {
    return (
        <div className={`${styles.card2D} ${className}`} style={{ backgroundColor: color, display: display }}>
            {children}
        </div>
    );
}

export default Card2D;