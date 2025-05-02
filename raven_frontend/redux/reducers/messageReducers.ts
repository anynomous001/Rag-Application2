import {
    LLM_MESSAGE_REQUEST,
    LLM_MESSAGE_SUCCESS,
    LLM_MESSAGE_FAILURE,
} from '@/redux/actions/messageActions'
import { nanoid } from 'nanoid'

export type MessageType = {
    id: string,
    message: string,
    role: "Assistant" | "User",
    createdAt: string  // Changed from Date to string
}

const Initial_Message: MessageType[] = [{
    id: nanoid(),
    role: "Assistant",
    message: "Hello! I'm Cal, your AI assistant. Ask me anything about Naval Ravikant's wisdom from The Almanack of Naval Ravikant.",
    createdAt: new Date().toISOString()  // Convert Date to ISO string
}]

export const InitialState = {
    requestLoading: false,
    messages: Initial_Message,
}

export const messageReducer = (state = InitialState, action: any) => {
    switch (action.type) {
        case LLM_MESSAGE_REQUEST:
            return {
                requestLoading: true,
                messages: [...state.messages, {
                    ...action.payload,
                    createdAt: new Date().toISOString()  // Ensure createdAt is an ISO string
                }]
            }
        case LLM_MESSAGE_SUCCESS:
            return {
                requestLoading: false,
                messages: [...state.messages, {
                    ...action.payload,
                    createdAt: new Date().toISOString()  // Ensure createdAt is an ISO string
                }]
            }
        case LLM_MESSAGE_FAILURE:
            return {
                ...state,
                requestLoading: false,
            }
        default:
            return state;
    }
}