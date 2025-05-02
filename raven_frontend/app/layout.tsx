import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ReduxProvider } from "@/provider";
import { Toaster } from "sonner";
import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Raven AI",
  description: "Your AI pdf reader.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <ReduxProvider>
        <body
          className={` antialiased bg-background font-sans`}
        >
          {children}
          <Toaster position="top-center" />

        </body>
      </ReduxProvider>
    </html>
  );
}
