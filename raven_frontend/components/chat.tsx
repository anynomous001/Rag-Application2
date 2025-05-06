'use client'
import React from 'react'
import { nanoid } from 'nanoid'
import ChatMessage from './chatmessage'
import { cn } from '@/lib/utils'
import { Button } from './ui/button'
import { Send } from 'lucide-react'
import { toast } from 'sonner'
import { MessageType } from '@/redux/reducers/messageReducers'
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '@/redux/store';
import { llmMessageFailure, llmMessageRequest, llmMessageSuccess } from '@/redux/actions/messageActions'
// import QuerySubmitSection from './querySubmitSection'
import axios from 'axios'



const Chat = () => {

    const dispatch = useDispatch();
    const { messages, requestLoading } = useSelector((state: RootState) => state.message)
    const [input, setInput] = React.useState("");
    const messagesEndRef = React.useRef<HTMLDivElement>(null);
    const textareaRef = React.useRef<HTMLTextAreaElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    React.useEffect(() => {
        scrollToBottom();
    }, [messages]);

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();

        if (!input.trim()) return;

        const userMessage: MessageType = {
            id: nanoid(),
            message: input.trim(),
            role: "User",
            createdAt: new Date().toISOString(),  // Convert to ISO string
        };

        dispatch(llmMessageRequest(userMessage));
        setInput("");

        try {
            const response = await axios.post(
                `/api/ask`,  // Use relative path for API route
                { message: userMessage.message },
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            );

            console.log(response)
            // const response2 = 'this is response' demo response
            const assistantMessage: MessageType = {
                id: nanoid(),
                message: response.data.answer,
                role: "Assistant",
                createdAt: new Date().toISOString(),  // Convert to ISO string
            };

            dispatch(llmMessageSuccess(assistantMessage));
        } catch (error) {
            console.error("Error getting response:", error);
            toast.error("Failed to get a response. Please try again.");
        } finally {
            dispatch(llmMessageFailure("Failed to get a response. Please try again."));
        }
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <div className="flex flex-col h-full">
            <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-w-2 scrollbar-thumb-blue scrollbar-thumb-rounded scrollbar-track-blue-lighter">
                {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                ))}

                {requestLoading && (
                    <div className="flex items-center space-x-2 bg-white p-4 rounded-lg max-w-3xl mx-auto">
                        <div className="flex space-x-2">
                            <div className="h-2 w-2 bg-blue-500 rounded-full animate-pulse"></div>
                            <div className="h-2 w-2 bg-blue-500 rounded-full animate-pulse delay-75"></div>
                            <div className="h-2 w-2 bg-blue-500 rounded-full animate-pulse delay-150"></div>
                        </div>
                        <div className="text-sm text-gray-500">Cal is thinking...</div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <div className="border-t bg-white p-4 flex justify-center">
                <form onSubmit={handleSubmit} className="container flex gap-2 items-end">
                    <textarea
                        ref={textareaRef}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask a question about Naval Ravikant's wisdom..."
                        className={cn(
                            "flex-1 resize-none max-h-46 min-h-20 p-2",
                            input.split("\n").length > 1 ? "h-24" : "h-10"
                        )}
                        rows={1}
                        disabled={requestLoading}
                    />
                    <Button
                        type="submit"
                        size="icon"
                        disabled={requestLoading || !input.trim()}
                        className="h-10 w-10"
                    >
                        <Send className="h-4 w-4" />
                    </Button>
                </form>
            </div>
        </div>
    )
}

export default Chat