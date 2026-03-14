import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "System Design Interview Coach",
  description:
    "AI-powered coach for practicing system design interviews with structured tasks and rubric scoring.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <nav className="border-b px-6 py-3 flex items-center gap-6 text-sm">
          <Link href="/" className="font-bold text-base">
            SD Coach
          </Link>
          <Link href="/sessions" className="hover:underline">
            Sessions
          </Link>
        </nav>
        {children}
      </body>
    </html>
  );
}
