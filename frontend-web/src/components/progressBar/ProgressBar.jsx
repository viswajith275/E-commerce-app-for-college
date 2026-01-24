import styles from './ProgressBar.module.css';

const ProgressBar = ({ className = "", progress = 0, color = "white"}) => {

    return (
        <div className={`${styles.container} ${className}`}>
            <div className={styles.bar} style = {{width: `${progress}%`, backgroundColor: color}}></div>
        </div>
    );
}

export default ProgressBar;