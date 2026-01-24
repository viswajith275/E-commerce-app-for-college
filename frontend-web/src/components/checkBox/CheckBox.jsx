import styles from './CheckBox.module.css';

const CheckBox = ( {size = 16} ) => {
    return (
        <label className={styles.container}>
            <input type="checkbox" style={{fontSize: size}} />
            <div className={styles.checkmark}></div>
        </label>
    );
}

export default CheckBox;