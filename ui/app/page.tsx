"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function Home() {
  const [status, setStatus] = useState<string>("checking...");

  useEffect(() => {
    const fetchHealth = async () => {
      try {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/health`
        );
        const data = await res.json();
        setStatus(data.status);
      } catch {
        setStatus("backend not reachable");
      }
    };

    fetchHealth();
  }, []);

  const isOk = status === "ok";

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 gap-8">
      <h1 className="text-4xl font-bold">System Design Interview Coach</h1>
      <p className="text-lg text-gray-600 max-w-xl text-center">
        Practice system design interviews with an AI-powered coach.
        Create a session, answer structured tasks, and get scored against an
        8&#8209;category rubric.
      </p>

      <div className="flex gap-4 items-center">
        <Link
          href="/sessions"
          className="bg-black text-white rounded px-6 py-3 text-lg font-semibold hover:opacity-80 transition-opacity"
        >
          Go to Sessions
        </Link>
      </div>

      <div className="text-sm text-gray-500">
        Backend:{" "}
        <span className={isOk ? "text-green-600" : "text-red-500"}>
          {status}
        </span>
      </div>
    </main>
  );
}
