"use client";

import { useEffect, useState } from "react";

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

export default function SessionsPage() {
  const [title, setTitle] = useState("");
  const [sessions, setSessions] = useState<Session[]>([]);
  const [error, setError] = useState<string>("");

  const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL;

  const loadSessions = async () => {
    setError("");
    try {
      const res = await fetch(`${apiBase}/sessions`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = (await res.json()) as Session[];
      setSessions(data);
    } catch (e) {
      setError("Failed to load sessions");
    }
  };

  const createSession = async () => {
    setError("");
    try {
      const res = await fetch(`${apiBase}/sessions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setTitle("");
      await loadSessions();
    } catch (e) {
      setError("Failed to create session");
    }
  };

  useEffect(() => {
    loadSessions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <main className="min-h-screen p-10 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Sessions</h1>

      <div className="flex gap-3 mb-6">
        <input
          className="border rounded px-3 py-2 w-full"
          placeholder="Session title (e.g., Design a Rate Limiter)"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button
          className="bg-black text-white rounded px-4 py-2"
          onClick={createSession}
          disabled={!title.trim()}
        >
          Create
        </button>
      </div>

      {error && <div className="text-red-600 mb-4">{error}</div>}

      <div className="space-y-3">
        {sessions.map((s) => (
          <div key={s.id} className="border rounded p-4">
            <div className="flex justify-between items-center">
              <div>
                <div className="font-semibold">{s.title}</div>
                <div className="text-sm text-gray-500">
                  {new Date(s.created_at).toLocaleString()}
                </div>
              </div>
              <div className="text-sm text-gray-700">
                {s.events?.length ?? 0} events
              </div>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}
