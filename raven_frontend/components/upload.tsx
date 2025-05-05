import React from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import FileUploader from "@/components/fileuploader";

const UploadPage = () => {
    return (
        <div className='relative flex justify-center w-full h-screen items-center'>
            <div className='absolute inset-0 bg-green-400/10 backdrop-blur-sm'></div>

            <div className='relative z-10  p-6 w-1/2 md:w-1/4 bg-white/90 rounded-lg shadow-xl hover:shadow-2xl transition-all duration-300'>
                <span className='block text-lg font-medium mb-4 text-slate-700'>Upload a PDF document</span>
                <FileUploader />
            </div>
        </div>
    )
}

export default UploadPage