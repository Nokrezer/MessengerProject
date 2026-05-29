import { authService } from "@/src/services/fetchServices/authService.ts";

import {showError} from "@/src/shared/appMessages";

import { useEffect, useState, useCallback } from "react";

export function useUpdateAccessTokenEvent() {
    const [loading, setLoading] = useState(true);

    const updateToken = useCallback(() => {(async() => {
        try{
            if(!authService.refreshToken || authService.refreshToken === ""){//Если токена нету
                // setUpdated(false);
                setLoading(false);
            }

            const accessToken = await authService.updateAccessToken();
            
            if(!accessToken)
                setLoading(false);
            
            setLoading(false);
        }catch(error){
            showError(error);
            // setUpdated(false);
            setLoading(false);
        }
    })()}, []);
    
    return {updateToken, loading};
}

// export function useUpdateAccessToken() {
//     const [loading, setLoading] = useState(true);
//     const [isUpdated, setUpdated] = useState(false);

//     useEffect(() => {(async() => {
//         try{
//             if(!authService.refreshToken || authService.refreshToken === ""){//Если токена нету
//                 setUpdated(false);
//                 setLoading(false);
//                 return;
//             }

//             const accessToken = await authService.updateAccessToken();
            
//             if(!accessToken)
//                 setLoading(false);
            
//             setUpdated(true);
//             setLoading(false);
//         }catch(error){
//             showError(error);
//             setUpdated(false);
//             setLoading(false);
//         }
//     })()}, []);

//     if(loading)
//         return {isUpdated, loading};

//     return {isUpdated, loading};
// }