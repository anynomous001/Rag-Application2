import Chat from '@/components/chat'
import Header from '@/components/header'
import React from 'react'

const Page = () => {
    return (
        <div className="flex flex-col h-screen">
            <Header />
            <main className="flex-1 overflow-hidden">
                <Chat />
            </main>
        </div>
    )
}

export default Page