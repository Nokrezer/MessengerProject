import { chatService } from "@/src/services/fetchServices/chatService";
import { authService } from "../services/fetchServices/authService";
import { useEffect, useState } from "react";

export function useGetChats(){
    const [loading, setLoading] = useState(true);
    const [chats, setChats] = useState();

    useEffect(() => {(async() => {
        const chats = await chatService.getChats();
        
        setChats(chats);
        setLoading(false);
    })()}, []);
    
    return {chats, loading};
}