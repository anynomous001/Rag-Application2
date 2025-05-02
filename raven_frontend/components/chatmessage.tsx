import React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { MessageType } from "@/redux/reducers/messageReducers";

interface ChatMessageProps {
    message: MessageType;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
    const isUser = message.role === "User";

    return (
        <div className={cn(
            "flex gap-3 p-4 rounded-lg max-w-3xl mx-auto",
            isUser ? "bg-chat-user" : "bg-chat-assistant"
        )}>
            <Avatar className="h-8 w-8">
                {isUser ? (
                    <AvatarFallback className="bg-slate-700 text-white">U</AvatarFallback>
                ) : (
                    <>
                        <AvatarImage src="/placeholder.svg" alt="Cal" />
                        <AvatarFallback className="bg-blue-500 text-white">Cal</AvatarFallback>
                    </>
                )}
            </Avatar>

            <div className="flex flex-col">
                <div className="text-xl font-medium mb-1 text-slate-800/50">
                    {isUser ? "You" : "Cal"}
                </div>
                <div className="text-sm whitespace-pre-wrap bg-gray-400/10 rounded-2xl p-4">
                    {message.message}
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;