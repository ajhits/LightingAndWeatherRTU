import { onValue, ref } from "firebase/database";
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