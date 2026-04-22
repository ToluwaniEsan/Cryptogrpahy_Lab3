import { spawnSync } from "child_process";
import path from "path";
import { NextResponse } from "next/server";

const MAX_BODY_BYTES = 512 * 1024;
const PYTHON_TIMEOUT_MS = 10_000;

/**
 * Parent of `web/` when `npm run dev` is executed from `web/` (default).
 * Override with env `CIPHER_REPO_ROOT` if you start Next.js from another cwd.
 */
function getRepoRoot(): string {
  if (process.env.CIPHER_REPO_ROOT) {
    return path.resolve(process.env.CIPHER_REPO_ROOT);
  }
  return path.resolve(process.cwd(), "..");
}

function getPythonExe(): string {
  return process.env.PYTHON_EXE ?? (process.platform === "win32" ? "python" : "python3");
}

type CipherPayload = {
  mode?: string;
  text?: unknown;
  key?: unknown;
  rails?: unknown;
};

export async function POST(req: Request) {
  let raw: string;
  try {
    raw = await req.text();
  } catch {
    return NextResponse.json({ ok: false, error: "Could not read body." }, { status: 400 });
  }

  if (raw.length > MAX_BODY_BYTES) {
    return NextResponse.json({ ok: false, error: "Request too large." }, { status: 413 });
  }

  let body: CipherPayload;
  try {
    body = JSON.parse(raw) as CipherPayload;
  } catch {
    return NextResponse.json({ ok: false, error: "Invalid JSON." }, { status: 400 });
  }

  const mode = body.mode;
  const text = body.text;
  const key = body.key;
  const rails = body.rails;

  if (mode !== "encrypt" && mode !== "decrypt") {
    return NextResponse.json(
      { ok: false, error: 'mode must be "encrypt" or "decrypt".' },
      { status: 400 }
    );
  }
  if (typeof text !== "string" || typeof key !== "string") {
    return NextResponse.json({ ok: false, error: "text and key must be strings." }, { status: 400 });
  }
  if (typeof rails !== "number" || !Number.isInteger(rails)) {
    return NextResponse.json({ ok: false, error: "rails must be an integer." }, { status: 400 });
  }
  if (rails < 2) {
    return NextResponse.json({ ok: false, error: "rails must be at least 2." }, { status: 400 });
  }

  const repoRoot = getRepoRoot();

  const payload = JSON.stringify({ mode, text, key, rails });
  const python = getPythonExe();

  const proc = spawnSync(python, ["cipher_bridge.py"], {
    cwd: repoRoot,
    input: payload,
    encoding: "utf-8",
    timeout: PYTHON_TIMEOUT_MS,
    maxBuffer: 10 * 1024 * 1024,
    windowsHide: true,
  });

  if (proc.error) {
    return NextResponse.json(
      {
        ok: false,
        error: `Could not run Python (${python}). Install Python 3 and ensure it is on PATH, or set PYTHON_EXE.`,
      },
      { status: 500 }
    );
  }

  if (proc.signal) {
    return NextResponse.json({ ok: false, error: "Cipher process was interrupted." }, { status: 500 });
  }

  const out = proc.stdout?.trim() ?? "";
  if (!out) {
    return NextResponse.json(
      {
        ok: false,
        error:
          proc.stderr?.trim() ||
          "No output from cipher bridge. Check that Python can import cpt_cipher from the project root.",
      },
      { status: 500 }
    );
  }

  try {
    const parsed = JSON.parse(out) as { ok?: boolean; result?: string; error?: string };
    if (!parsed.ok) {
      const message = parsed.error ?? "Cipher error.";
      return NextResponse.json({ ok: false, error: message }, { status: 400 });
    }
    return NextResponse.json({ ok: true, result: parsed.result ?? "" });
  } catch {
    return NextResponse.json(
      {
        ok: false,
        error: `Unexpected output from Python: ${out.slice(0, 200)}`,
      },
      { status: 500 }
    );
  }
}
