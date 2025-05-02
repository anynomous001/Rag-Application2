// 'use server'

import { toast } from 'sonner'
import axios from 'axios'
import dotenv from 'dotenv'
import { MessageType } from '@/redux/reducers/messageReducers'

dotenv.config()

export const SendQueryAction = async (message: string) => {
    try {
        const response = await axios.post(
            `/api/ask`,  // Use relative path for API route
            { message },
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        return response.data.content;
    } catch (error) {
        console.error('Error in SendQueryAction:', error);
        throw error;
    }
}