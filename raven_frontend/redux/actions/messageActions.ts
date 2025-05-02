import { MessageType } from "../reducers/messageReducers";

export const LLM_MESSAGE_REQUEST = 'LLM_MESSAGE_REQUEST'
export const LLM_MESSAGE_SUCCESS = 'LLM_MESSAGE_SUCCESS'
export const LLM_MESSAGE_FAILURE = 'LLM_MESSAGE_FAILURE'


export const llmMessageRequest = (userResponse: MessageType) => ({
    type: LLM_MESSAGE_REQUEST,
    payload: userResponse,

});
export const llmMessageSuccess = (llmResponse: MessageType) => ({
    type: LLM_MESSAGE_SUCCESS,
    payload: llmResponse,
});


//error is in state but do not have any usecase now

export const llmMessageFailure = (error: string) => ({
    type: LLM_MESSAGE_FAILURE,
    payload: error,
});