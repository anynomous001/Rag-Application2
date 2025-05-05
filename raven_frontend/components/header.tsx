'use client'
import React from "react";
import { Button } from "@/components/ui/button";
import { Upload } from "lucide-react";
import FileUploader from "@/components/fileuploader";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { redirect } from "next/navigation";


const Header = () => {

    // const router = useRouter()


    return (
        <header className="border-b bg-white flex justify-center">
            <div className="container flex items-center justify-between h-16">
                <div className="flex items-center gap-2">
                    <h1 className="text-xl font-bold tracking-tighter">Raven</h1>
                    <span className="bg-black text-white text-xs px-2 py-1 rounded-full">The PDF AI</span>
                </div>

                <Button onClick={() => redirect('/')} variant="outline" size="sm" className="flex gap-2">
                    <Upload size={16} />
                    <span>Upload PDF</span>
                </Button>

            </div>
        </header>)
}

export default Header