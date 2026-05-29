import {useState, useEffect} from "react";

import { loadUserData } from "@/src/useCase/initApp";

//Загрузка всех пользовательских данных при входе в приложение
export function useLoadUserData(){
    const [loading, setLoading] = useState(true);
    const [userLogged, setLogged] = useState(false);

    useEffect(() => {(async() => {
        const result = await loadUserData();
        
        setLogged(result);
        setLoading(false);
    })()}, []);

    return {loading, userLogged};
}