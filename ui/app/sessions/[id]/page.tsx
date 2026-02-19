"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

type Event = {
  id: string;
  timestamp: string;
  type: string;
  content: string;
  payload?: Record<string, unknown> | null;
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

  const [filter, setFilter] = useState<"all" | "constitution" | "specify" | "plan">(
    "all"
  );

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

    const filteredEvents =
    filter === "all"
        ? session.events
        : session.events.filter((e) => {
            if (filter === "specify") {
            return e.type.startsWith("specify") || e.type.startsWith("specifier");
            }
            return e.type.startsWith(filter);
        });


  return (
    <main className="min-h-screen p-10 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">{session.title}</h1>
      <div className="text-sm text-gray-500 mb-8">
        Created: {new Date(session.created_at).toLocaleString()}
      </div>

      <h2 className="text-xl font-semibold mb-4">Timeline</h2>

      <div className="flex gap-2 mb-6">
        {(["all", "constitution", "specify", "plan"] as const).map((f) => (
          <button
            key={f}
            className={`border rounded px-3 py-1 text-sm ${
              filter === f ? "bg-black text-white" : "bg-white"
            }`}
            onClick={() => setFilter(f)}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="space-y-3">
        {filteredEvents.map((e) => (
          <div key={e.id} className="border rounded p-4">
            <div className="flex justify-between items-start gap-4">
              <div>
                <div className="font-mono text-sm text-gray-600">{e.type}</div>
                <div className="mt-1">{e.content}</div>
                {e.payload && (
                <details className="mt-3">
                    <summary className="cursor-pointer text-sm text-gray-600">
                    Show payload
                    </summary>

                    {"instructions_md" in e.payload ? (
                    <div className="mt-2 text-sm bg-gray-50 border rounded p-4 whitespace-pre-wrap">
                        {(e.payload as any).instructions_md}
                    </div>
                    ) : (
                    <pre className="mt-2 text-xs bg-gray-50 border rounded p-3 overflow-x-auto whitespace-pre-wrap break-words">
                        {JSON.stringify(e.payload, null, 2)}
                    </pre>
                    )}
                </details>
                )}
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
