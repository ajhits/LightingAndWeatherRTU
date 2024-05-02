import { onValue, ref, set } from "firebase/database";
import { database } from "./Configuration";

export const getHistory = async () => {
    return new Promise((resolve, reject) => {
        try {
            const keyRef = ref(database, `History/`);
            onValue(keyRef, (snapshot) => {

                const data = snapshot.val();
                resolve(data)

            }, (error) => {
                reject(error);
            });
        } catch (err) {
            console.error(err);
            reject(null)
        }

    })
}

// **************** relay **************** //
export const updateRelay = async (props) => {
    try {
        const keyRef = ref(database, `relay/${props.relay}/`);
        
        set(keyRef,props.value);
 
    } catch (err) {
        console.error(err);
    }
}

export const getTimer = async () => {
    return new Promise((resolve, reject) => {
        try {
            const keyRef = ref(database, `Timer/`);
            onValue(keyRef, (snapshot) => {

                const data = snapshot.val();
                resolve(data)

            }, (error) => {
                reject(error);
            });
        } catch (err) {
            console.error(err);
            reject(null)
        }

    })
}

// **************** set Timer **************** //
export const setTimer = async (props) => {
    try {
        const keyRef = ref(database, `Timer/`);
        
        set(keyRef,props.timer);
 
    } catch (err) {
        console.error(err);
    }
}