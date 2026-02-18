"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type Event = {
  id: string;
  timestamp: string;
  type: string;
  content: string;
};

type Session = {
  id: string;
  created_at: string;
  title: string;
  events: Event[];
};

export default function SessionDetailsPage() {
  const params = useParams<{ id: string }>();
  const sessionId = params.id;

  const [session, setSession] = useState<Session | null>(null);
  const [error, setError] = useState("");

  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL;

  useEffect(() => {
    const load = async () => {
      setError("");
      try {
        const res = await fetch(`${apiBase}/sessions/${sessionId}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = (await res.json()) as Session;
        setSession(data);
      } catch (e) {
        setError("Failed to load session");
      }
    };

    load();
  }, [apiBase, sessionId]);

  if (error) {
    return (
      <main className="min-h-screen p-10 max-w-4xl mx-auto">
        <div className="text-red-600">{error}</div>
      </main>
    );
  }

  if (!session) {
    return (
      <main className="min-h-screen p-10 max-w-4xl mx-auto">
        <div>Loading...</div>
      </main>
    );
  }

  return (
    <main className="min-h-screen p-10 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">{session.title}</h1>
      <div className="text-sm text-gray-500 mb-8">
        Created: {new Date(session.created_at).toLocaleString()}
      </div>

      <h2 className="text-xl font-semibold mb-4">Timeline</h2>

      <div className="space-y-3">
        {session.events.map((e) => (
          <div key={e.id} className="border rounded p-4">
            <div className="flex justify-between items-start gap-4">
              <div>
                <div className="font-mono text-sm text-gray-600">{e.type}</div>
                <div className="mt-1">{e.content}</div>
              </div>
              <div className="text-xs text-gray-500 whitespace-nowrap">
                {new Date(e.timestamp).toLocaleString()}
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
