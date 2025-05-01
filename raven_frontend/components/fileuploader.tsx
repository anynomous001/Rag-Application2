'use client'
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Upload } from "lucide-react";


const FileUploader = () => {
    const [file, setFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (!selectedFile) return;

        if (selectedFile.type !== "application/pdf") {
            toast.error("Please upload a PDF file");
            return;
        }

        setFile(selectedFile);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!file) {
            toast.error('Please upload a PDF file!')
        }


        try {
            setUploading(true)

            //backend Call
            new Promise(resolve => setTimeout(resolve, 2000))
            toast.success("PDF uploaded successfully.")
        } catch (error: any) {
            toast.error(error.message)
            console.error(error.message)
        } finally {
            setUploading(false)
            setFile(null)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <div className="border-2 border-dashed rounded-lg p-6 border-gray-300 hover:border-primary transition-colors cursor-pointer">
                <input
                    type="file"
                    id="file-upload"
                    className="hidden"
                    onChange={handleFileChange}
                    accept=".pdf"
                />
                <label htmlFor="file-upload" className="flex flex-col items-center cursor-pointer">
                    <Upload className="w-10 h-10 text-gray-400 mb-2" />
                    <p className="text-sm font-medium">
                        {file ? file.name : "Click to upload or drag and drop"}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">PDF (max 20MB)</p>
                </label>
            </div>


            {file && (
                <div className="flex items-center justify-between bg-secondary p-3 rounded-lg">
                    <span className="text-sm font-medium truncate max-w-[200px]">{file.name}</span>
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setFile(null)}
                        type="button"
                    >
                        Remove
                    </Button>
                </div>
            )}

            <Button
                type="submit"
                className="w-full"
                disabled={!file || uploading}
            >
                {uploading ? "Uploading..." : "Upload PDF"}
            </Button>
        </form>
    )
}

export default FileUploader