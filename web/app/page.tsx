"use client";

import { useState } from "react";

import { FloatingStudentNames } from "./components/FloatingStudentNames";

type Mode = "encrypt" | "decrypt";

export default function Home() {
  const [mode, setMode] = useState<Mode>("encrypt");
  const [text, setText] = useState("");
  const [key, setKey] = useState("");
  const [rails, setRails] = useState(3);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const res = await fetch("/api/cipher", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mode,
          text,
          key,
          rails: Math.floor(Number(rails)),
        }),
      });
      const data = (await res.json()) as { ok?: boolean; result?: string; error?: string };
      if (!res.ok || !data.ok) {
        setError(data.error ?? `Request failed (${res.status}).`);
        return;
      }
      setResult(data.result ?? "");
    } catch {
      setError("Network error — is the dev server running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative min-h-screen overflow-x-hidden">
      <FloatingStudentNames />
      {/* Layered wavy gold / white / grey background */}
      <div
        className="pointer-events-none fixed inset-0 z-0 bg-gradient-to-br from-stone-200 via-[#faf8f5] to-[#c4c4c9]"
        aria-hidden
      />
      <div
        className="pointer-events-none fixed inset-0 z-0 bg-[radial-gradient(ellipse_120%_80%_at_50%_-20%,rgba(235,200,95,0.48),transparent_55%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none fixed inset-0 z-0 bg-[radial-gradient(ellipse_80%_50%_at_100%_100%,rgba(156,163,175,0.45),transparent_50%)]"
        aria-hidden
      />

      <svg
        className="pointer-events-none fixed bottom-0 left-1/2 z-0 w-[min(140%,1800px)] -translate-x-1/2 text-[#ecc94b]/45"
        viewBox="0 0 1440 320"
        preserveAspectRatio="none"
        aria-hidden
      >
        <path
          fill="currentColor"
          d="M0,160L48,149.3C96,139,192,117,288,117.3C384,117,480,139,576,154.7C672,171,768,181,864,165.3C960,149,1056,107,1152,101.3C1248,96,1344,128,1392,144L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
        />
      </svg>
      <svg
        className="pointer-events-none fixed -bottom-8 left-1/2 z-0 w-[min(160%,2000px)] -translate-x-1/2 text-[#9ca3af]/50"
        viewBox="0 0 1440 320"
        preserveAspectRatio="none"
        aria-hidden
      >
        <path
          fill="currentColor"
          d="M0,224L60,213.3C120,203,240,181,360,181.3C480,181,600,203,720,208C840,213,960,203,1080,186.7C1200,171,1320,149,1380,138.7L1440,128L1440,320L1380,320C1320,320,1200,320,1080,320C960,320,840,320,720,320C600,320,480,320,360,320C240,320,120,320,60,320L0,320Z"
        />
      </svg>
      <svg
        className="pointer-events-none fixed bottom-12 left-1/2 z-0 w-[min(120%,1600px)] -translate-x-1/2 text-white/90"
        viewBox="0 0 1440 200"
        preserveAspectRatio="none"
        aria-hidden
      >
        <path
          fill="currentColor"
          d="M0,96L80,101.3C160,107,320,117,480,112C640,107,800,85,960,90.7C1120,96,1280,128,1360,144L1440,160L1440,200L1360,200C1280,200,1120,200,960,200C800,200,640,200,480,200C320,200,160,200,80,200L0,200Z"
        />
      </svg>

      <div className="relative z-10 mx-auto flex min-h-screen max-w-4xl flex-col items-center justify-center px-4 pb-16 pt-28 sm:px-6 sm:pt-32">
        <div className="w-full max-w-xl rounded-[2rem] border border-white/55 bg-white/45 p-8 shadow-[0_25px_80px_-15px_rgba(0,0,0,0.15)] backdrop-blur-2xl ring-1 ring-[#fde68a]/90 sm:p-10">
          <header className="mb-8 text-center">
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.25em] text-[color:var(--gold-deep)]">
              Cryptography Lab
            </p>
            <h1 className="bg-gradient-to-r from-[#78716c] via-[#e6bc2f] to-[#78716c] bg-clip-text text-3xl font-semibold tracking-tight text-transparent sm:text-4xl">
              CPT Cipher
            </h1>
          </header>

          <form onSubmit={handleSubmit} className="flex flex-col gap-6">
            <div className="flex rounded-2xl border border-white/60 bg-white/30 p-1 shadow-inner ring-1 ring-zinc-200/40">
              <button
                type="button"
                onClick={() => setMode("encrypt")}
                className={`flex-1 rounded-xl px-4 py-2.5 text-sm font-medium transition ${
                  mode === "encrypt"
                    ? "bg-gradient-to-br from-[#f0d060] to-[#d4af37] text-white shadow-md"
                    : "text-zinc-600 hover:bg-white/40"
                }`}
              >
                Encrypt
              </button>
              <button
                type="button"
                onClick={() => setMode("decrypt")}
                className={`flex-1 rounded-xl px-4 py-2.5 text-sm font-medium transition ${
                  mode === "decrypt"
                    ? "bg-gradient-to-br from-[#f0d060] to-[#d4af37] text-white shadow-md"
                    : "text-zinc-600 hover:bg-white/40"
                }`}
              >
                Decrypt
              </button>
            </div>

            <label className="flex flex-col gap-2">
              <span className="text-sm font-medium text-zinc-700">
                {mode === "encrypt" ? "Plaintext" : "Ciphertext"}
              </span>
              <textarea
                required
                rows={5}
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder={
                  mode === "encrypt" ? "Enter message…" : "Paste ciphertext…"
                }
                className="rounded-xl border border-white/70 bg-white/50 px-4 py-3 text-zinc-800 shadow-inner outline-none ring-1 ring-zinc-200/50 placeholder:text-zinc-400 focus:border-amber-200/90 focus:ring-2 focus:ring-amber-200/70"
              />
            </label>

            <div className="grid gap-4 sm:grid-cols-2">
              <label className="flex flex-col gap-2">
                <span className="text-sm font-medium text-zinc-700">Keyword</span>
                <input
                  type="text"
                  required
                  value={key}
                  onChange={(e) => setKey(e.target.value)}
                  placeholder="e.g. KEY"
                  className="rounded-xl border border-white/70 bg-white/50 px-4 py-3 text-zinc-800 shadow-inner outline-none ring-1 ring-zinc-200/50 placeholder:text-zinc-400 focus:border-amber-200/90 focus:ring-2 focus:ring-amber-200/70"
                />
              </label>
              <label className="flex flex-col gap-2">
                <span className="text-sm font-medium text-zinc-700">Rails (≥ 2)</span>
                <input
                  type="number"
                  required
                  min={2}
                  step={1}
                  value={rails}
                  onChange={(e) => setRails(Number(e.target.value))}
                  className="rounded-xl border border-white/70 bg-white/50 px-4 py-3 text-zinc-800 shadow-inner outline-none ring-1 ring-zinc-200/50 focus:border-amber-200/90 focus:ring-2 focus:ring-amber-200/70"
                />
              </label>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="rounded-2xl bg-gradient-to-r from-[#ecc94b] via-[#f0d050] to-[#d4af37] px-6 py-3.5 text-center text-sm font-semibold text-white shadow-lg shadow-amber-700/15 transition hover:brightness-105 disabled:opacity-60"
            >
              {loading ? "Running…" : mode === "encrypt" ? "Encrypt" : "Decrypt"}
            </button>
          </form>

          {(result !== null || error) && (
            <div className="mt-8 rounded-2xl border border-white/60 bg-white/35 p-5 backdrop-blur-md ring-1 ring-zinc-200/40">
              <p className="mb-2 text-xs font-semibold uppercase tracking-wider text-zinc-500">
                {error ? "Error" : mode === "encrypt" ? "Ciphertext" : "Plaintext"}
              </p>
              {error ? (
                <p className="font-mono text-sm text-red-700">{error}</p>
              ) : (
                <p className="break-all font-mono text-sm leading-relaxed text-zinc-800">{result}</p>
              )}
            </div>
          )}
        </div>

        <p className="mt-10 max-w-md text-center text-xs text-zinc-500">
          Powered by Python <code className="rounded bg-white/40 px-1 py-0.5 font-mono text-zinc-600">cpt_cipher</code> via{" "}
          <code className="rounded bg-white/40 px-1 py-0.5 font-mono text-zinc-600">cipher_bridge.py</code>. Requires Python 3 on the server machine.
        </p>
      </div>
    </div>
  );
}
