export type TeamMember = {
  name: string;
  /** Full LinkedIn profile URL; omit until you have it — chip stays non-clickable */
  linkedinUrl?: string;
};

export const TEAM_MEMBERS: readonly TeamMember[] = [
  {
    name: "Toluwani Esan",
    linkedinUrl: "https://www.linkedin.com/in/esan-toluwani",
  },
  {
    name: "Emmanuel Aina",
    linkedinUrl: "https://www.linkedin.com/in/emmanuelaina4",
  },
  {
    name: "Solomon Agyire",
    linkedinUrl: "https://www.linkedin.com/in/solomon-agyire",
  },
  {
    name: "Olasubomi Awodipe",
    linkedinUrl: "https://www.linkedin.com/in/olasubomiawodipe",
  },
  {
    name: "Osamwengumwenro Oni-Ojo",
    linkedinUrl: "https://www.linkedin.com/in/gumwenoniojo",
  },
  {
    name: "Yin Chih Lan",
    linkedinUrl: "https://www.linkedin.com/in/scott-lan-6264ab383",
  },
];

export const STUDENT_NAMES = TEAM_MEMBERS.map((m) => m.name);

const chipClassName =
  "inline-flex max-w-full rounded-full border border-white/85 bg-white/55 px-3 py-1.5 text-xs font-medium text-[color:var(--gold-mid)] shadow-sm backdrop-blur-md transition hover:bg-white/70 sm:text-sm";

/** Fixed credits strip at the top — frosted bar with individual frosted name chips in gold. */
export function FloatingStudentNames() {
  return (
    <header
      className="fixed inset-x-0 top-0 z-20 px-3 pt-3 sm:px-5"
      aria-label="Students who contributed to this project"
    >
      <div className="mx-auto max-w-5xl rounded-b-[1.75rem] border border-white/75 bg-white/60 px-4 py-3 shadow-[0_14px_44px_-14px_rgba(180,140,40,0.25)] backdrop-blur-2xl ring-1 ring-[color:var(--gold-light)]/70">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
          <p className="shrink-0 text-[10px] font-semibold uppercase tracking-[0.22em] text-[color:var(--gold-deep)] sm:text-xs">
            Team
          </p>
          <ul className="flex list-none flex-wrap gap-2">
            {TEAM_MEMBERS.map(({ name, linkedinUrl }) => (
              <li key={name}>
                {linkedinUrl ? (
                  <a
                    href={linkedinUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`${chipClassName} underline-offset-2 hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-[color:var(--gold-mid)] focus-visible:ring-offset-2 focus-visible:ring-offset-white/50`}
                    aria-label={`${name} on LinkedIn (opens in a new tab)`}
                  >
                    {name}
                  </a>
                ) : (
                  <span className={chipClassName}>{name}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </header>
  );
}
