"use client";

import { useEffect, useState } from "react";

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
      } catch (err) {
        setStatus("backend not reachable");
      }
    };

    fetchHealth();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-3xl font-bold mb-6">
        System Design Interview Coach
      </h1>
      <div className="text-xl">
        Backend status:{" "}
        <span className="font-semibold text-green-600">{status}</span>
      </div>
    </main>
  );
}
