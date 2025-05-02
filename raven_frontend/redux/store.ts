import { configureStore } from '@reduxjs/toolkit'
import { messageReducer } from './reducers/messageReducers'


const store = configureStore({
    reducer: {
        message: messageReducer,
    }

})


export type RootState = ReturnType<typeof store.getState>;
export default store;