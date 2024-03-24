import { doc, getDoc } from "firebase/firestore";
import { firestore } from "./Configuration";

// get userDetails
export const getUserDetails = (UID) =>{

    return new Promise(async (resolve,reject)=>{
  
  
    try {
      const docRef = doc(firestore, "user", "Rxn3VfEnlOgSxlGQMYwmiTkhi4S2"); // Assuming firestore is properly defined elsewhere
  
      const docSnap = await getDoc(docRef);
  
      if (docSnap.exists()) {
        const data = docSnap.data();
  
        resolve(data); // You can return the data or do whatever you want with it
      } else {
        console.log("User document does not exist!");
        reject(null); // Or handle the non-existence case accordingly
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
      reject(error); // Rethrow the error or handle it gracefully
    }
  })
  }