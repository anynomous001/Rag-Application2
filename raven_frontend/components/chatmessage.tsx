import React from "react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { cn } from "@/lib/utils";
import { MessageType } from "@/redux/reducers/messageReducers";
import { Copy } from "lucide-react";
import { toast } from "sonner";
import { IoPerson } from "react-icons/io5";
import { FaBrain } from "react-icons/fa";


interface ChatMessageProps {
    message: MessageType;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
    const isUser = message.role === "User";


    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(message.message);
            toast.success("Message copied to clipboard!");
        } catch (error) {
            toast.error("Failed to copy message");
        }
    };


    const renderFormattedText = (text: string) => {
        // Split by lines and trim extra spaces
        const lines = text.split(/\n/).map(line => line.trim());

        return lines.map((line, lineIndex) => {
            if (line.startsWith('*')) {
                const bulletContent = line.slice(2).trim(); // Remove "* " from start
                const parts = bulletContent.split(/(\*\*.*?\*\*)/g).map(part => part.trim());

                return (
                    <React.Fragment key={lineIndex}>
                        <div className="flex gap-2 ml-4 mb-2">
                            <span className="font-bold">•</span>
                            <div>
                                {parts.map((part, partIndex) => {
                                    if (part.startsWith('**') && part.endsWith('**')) {
                                        // Handle bold text
                                        return <strong key={partIndex}>{part.slice(2, -2)}</strong>;
                                    }
                                    return <span key={partIndex}>{part}</span>;
                                })}
                            </div>
                        </div>
                    </React.Fragment>
                );
            }

            // Handle regular text with italic markers
            if (line.includes('*')) {
                const parts = line.split(/(\*.*?\*)/g).map(part => part.trim());
                return (
                    <React.Fragment key={lineIndex}>
                        {parts.map((part, partIndex) => {
                            if (part.startsWith('*') && part.endsWith('*')) {
                                // Handle italic text
                                return <em key={partIndex}>{part.slice(1, -1)}</em>;
                            }
                            return <span key={partIndex}>{part}</span>;
                        })}
                        <br />
                        <br />
                    </React.Fragment>
                );
            }
            // Regular line without formatting
            return (
                <React.Fragment key={lineIndex}>
                    {line}
                    {lineIndex < lines.length - 1 && <br />}
                </React.Fragment>
            );
        });
    };







    return (
        <div className={cn(
            "flex gap-3 p-4 rounded-lg max-w-3xl mx-auto",
            isUser ? "bg-chat-user" : "bg-chat-assistant"
        )}>
            <Avatar className="h-8 w-8">
                {isUser ? (
                    <AvatarFallback className="bg-[#064e3b] text-white flex justify-center items-center">
                        <IoPerson />
                    </AvatarFallback>
                ) : (
                    <>
                        {/* <AvatarImage>
                            <IoPerson />
                        </AvatarImage> */}
                        {/* <AvatarImage src="/placeholder.svg" alt="Cal" /> */}
                        <AvatarFallback className="bg-[#059669] text-white flex justify-center items-center">
                            <FaBrain />
                        </AvatarFallback>
                    </>
                )}
            </Avatar>

            <div className="flex flex-col flex-1">
                <div className="flex justify-between items-center mb-1">
                    <div className="text-xl font-medium text-text-secondary">
                        {isUser ? "You" : "Raven"}
                    </div>
                    {!isUser && (
                        <button
                            onClick={handleCopy}
                            className="p-2 hover:bg-chat-user rounded-full transition-colors"
                            title="Copy message"
                        >
                            <Copy className="h-4 w-4 text-text-secondary" />
                        </button>
                    )}
                </div>
                <div className="text-sm whitespace-pre-wrap bg-white/50 rounded-2xl p-4 text-text-primary">
                    {renderFormattedText(message.message)}
                </div>
            </div>
        </div>
    );
};

export default ChatMessage;