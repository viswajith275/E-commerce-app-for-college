import styles from './Card.module.css';

const Card3D = ({ children, color = "white", display = "block", className = "" }) => {
    return (
        <div className={`${styles.card3D} ${className}`} style={{ backgroundColor: color, display: display }}>
            {children}
        </div>
    );
}

export default Card3D;