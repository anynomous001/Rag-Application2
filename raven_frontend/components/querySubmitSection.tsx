// import React from 'react'
// import { Button } from './ui/button'
// import { Send } from 'lucide-react'

// const QuerySubmitSection = () => {
//     return (
//         <div className="border-t bg-white p-4">
//             <form onSubmit={handleSubmit} className="container flex gap-2 items-end">
//                 <textarea
//                     ref={textareaRef}
//                     value={input}
//                     onChange={(e) => setInput(e.target.value)}
//                     onKeyDown={handleKeyDown}
//                     placeholder="Ask a question about Naval Ravikant's wisdom..."
//                     className={cn(
//                         "flex-1 resize-none max-h-36 min-h-10",
//                         input.split("\n").length > 1 ? "h-24" : "h-10"
//                     )}
//                     rows={1}
//                     disabled={requestLoading}
//                 />
//                 <Button
//                     type="submit"
//                     size="icon"
//                     disabled={requestLoading || !input.trim()}
//                     className="h-10 w-10"
//                 >
//                     <Send className="h-4 w-4" />
//                 </Button>
//             </form>
//         </div>
//     )
// }

// export default QuerySubmitSection