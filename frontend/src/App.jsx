import { useEffect, useMemo, useState } from 'react'

const chats = [
  {
    id: 1,
    title: 'Architecture overview',
    meta: 'Grounded answer',
    active: true,
  },
  {
    id: 2,
    title: 'Citation quality pass',
    meta: '4 sources',
    active: false,
  },
  {
    id: 3,
    title: 'Graph retrieval notes',
    meta: 'Needs evidence',
    active: false,
  },
]

const messages = [
  {
    role: 'user',
    text: 'What does the project plan say the local Agentic RAG system should do?',
  },
  {
    role: 'assistant',
    text: 'The MVP is a local-first RAG workflow that ingests documents, retrieves evidence through vector and graph routes, validates whether the context is strong enough, and returns a cited answer or an insufficient-evidence response.',
    citations: ['PLAN.md: Architecture And Behavior', 'PLAN.md: Acceptance Criteria'],
  },
  {
    role: 'user',
    text: 'Show me the retrieval path too.',
  },
  {
    role: 'assistant',
    text: 'A query is normalized, planned, routed through selected retrieval strategies, reranked, validated, and then handed to the answer generator with citation metadata and trace details.',
    citations: ['PLAN.md: Query Flow'],
  },
]

const traces = [
  ['understand', 'Intent normalized'],
  ['plan', 'Vector + graph selected'],
  ['retrieve', '7 chunks found'],
  ['validate', 'Evidence strong'],
]

function App() {
  const [prompt, setPrompt] = useState('')
  const [theme, setTheme] = useState(() => {
    const savedTheme = window.localStorage.getItem('theme')

    if (savedTheme === 'light' || savedTheme === 'dark') {
      return savedTheme
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  })

  const canSend = prompt.trim().length > 0
  const status = useMemo(() => (canSend ? 'Ready to query' : 'Waiting for input'), [canSend])
  const isDark = theme === 'dark'

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark)
    window.localStorage.setItem('theme', theme)
  }, [isDark, theme])

  function handleSubmit(event) {
    event.preventDefault()
    setPrompt('')
  }

  return (
    <main className="grid min-h-svh bg-slate-50 text-slate-950 transition-colors duration-200 dark:bg-[#031427] dark:text-[#d3e4fe] lg:grid-cols-[280px_minmax(0,1fr)]">
      <aside
        className="flex min-w-0 flex-col gap-5 border-b border-slate-200 bg-white px-4 py-4 dark:border-[#424754] dark:bg-[#0b1c30] lg:sticky lg:top-0 lg:h-svh lg:border-b-0 lg:border-r lg:px-4 lg:py-6"
        aria-label="Conversation history"
      >
        <div className="flex items-center gap-3">
          <div
            className="grid size-11 shrink-0 place-items-center rounded-lg bg-blue-500 text-sm font-bold text-white dark:bg-[#adc6ff] dark:text-[#002e6a]"
            aria-hidden="true"
          >
            AI
          </div>
          <div className="min-w-0">
            <p className="mb-1 text-xs font-medium uppercase leading-normal text-slate-500 dark:text-[#bec6e0]">
              Agentic RAG
            </p>
            <h1 className="truncate text-lg font-semibold leading-snug text-slate-950 dark:text-[#d3e4fe]">
              Intelligence Console
            </h1>
          </div>
        </div>

        <button
          className="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-lg bg-blue-500 px-4 text-sm font-semibold text-white transition hover:bg-blue-600"
          type="button"
        >
          <Icon name="plus" className="size-[18px]" />
          New query
        </button>

        <nav
          className="flex gap-2 overflow-x-auto pb-1 sm:grid sm:grid-cols-3 lg:grid-cols-1 lg:overflow-visible lg:pb-0"
          aria-label="Recent conversations"
        >
          {chats.map((chat) => (
            <button
              className={`relative grid min-h-16 min-w-52 gap-1 rounded-lg px-4 py-2.5 text-left text-slate-900 transition hover:bg-slate-100 dark:text-[#d3e4fe] dark:hover:bg-[#102034] sm:min-w-0 ${
                chat.active
                  ? 'bg-slate-100 before:absolute before:bottom-3 before:left-0 before:top-3 before:w-0.5 before:rounded-full before:bg-blue-500 dark:bg-[#102034]'
                  : ''
              }`}
              key={chat.id}
              type="button"
            >
              <span className="truncate text-sm leading-snug">{chat.title}</span>
              <small className="text-xs leading-normal text-slate-500 dark:text-[#c2c6d6]">{chat.meta}</small>
            </button>
          ))}
        </nav>

        <div className="mt-auto hidden min-h-11 items-center gap-3 rounded-lg bg-slate-100 p-3 text-xs leading-normal text-slate-500 dark:bg-[#102034] dark:text-[#c2c6d6] lg:flex">
          <span
            className="size-2 rounded-full bg-amber-400 shadow-[0_0_0_4px_rgba(251,191,36,0.18)]"
            aria-hidden="true"
          />
          <span>Local workspace connected</span>
        </div>
      </aside>

      <section className="grid min-h-svh min-w-0 grid-rows-[auto_1fr]">
        <header className="flex min-h-[88px] flex-col items-start justify-between gap-4 border-b border-slate-200 bg-white/90 px-4 py-4 dark:border-[#424754] dark:bg-[#031427]/90 sm:flex-row sm:items-center sm:px-6">
          <div className="min-w-0">
            <p className="mb-1 text-xs font-medium uppercase leading-normal text-slate-500 dark:text-[#bec6e0]">
              Grounded assistant
            </p>
            <h2 className="text-xl font-semibold leading-snug text-slate-950 dark:text-[#d3e4fe] sm:text-2xl">
              Ask over your indexed knowledge base
            </h2>
          </div>
          <div className="flex w-full flex-wrap items-center gap-2 sm:w-auto sm:justify-end">
            <div className="rounded-full border border-slate-200 bg-slate-100 px-3 py-1.5 text-xs leading-normal text-blue-600 dark:border-[#424754] dark:bg-[#0b1c30] dark:text-[#adc6ff]">
              {status}
            </div>
            <button
              className="inline-grid size-10 place-items-center rounded-lg border border-slate-200 bg-white text-slate-600 transition hover:bg-slate-100 hover:text-blue-600 dark:border-[#424754] dark:bg-[#0b1c30] dark:text-[#c2c6d6] dark:hover:bg-[#102034] dark:hover:text-[#adc6ff]"
              type="button"
              onClick={() => setTheme(isDark ? 'light' : 'dark')}
              aria-label={`Switch to ${isDark ? 'light' : 'dark'} mode`}
              title={`Switch to ${isDark ? 'light' : 'dark'} mode`}
            >
              <Icon name={isDark ? 'sun' : 'moon'} className="size-[18px]" />
            </button>
          </div>
        </header>

        <div className="grid min-h-0 lg:grid-cols-[minmax(0,1fr)_320px]">
          <section className="grid min-h-[calc(100svh-89px)] min-w-0 grid-rows-[1fr_auto]" aria-label="Chat feed">
            <div className="mx-auto flex w-full max-w-[800px] flex-col gap-4 px-4 py-7 sm:px-6 sm:py-10">
              {messages.map((message, index) => (
                <article
                  className={`max-w-full rounded-2xl px-4 py-3 text-slate-950 sm:max-w-[88%] ${
                    message.role === 'user'
                      ? 'self-end rounded-br bg-blue-500 text-white'
                      : 'self-start rounded-bl bg-white dark:bg-[#102034] dark:text-[#d3e4fe]'
                  }`}
                  key={`${message.role}-${index}`}
                >
                  <div className="mb-1.5 text-xs font-semibold leading-normal text-current/70">
                    {message.role === 'user' ? 'You' : 'Assistant'}
                  </div>
                  <p className="m-0 text-base leading-relaxed">{message.text}</p>
                  {message.citations && (
                    <div className="mt-3 flex flex-wrap gap-2" aria-label="Citations">
                      {message.citations.map((citation) => (
                        <span
                          className="rounded-lg bg-slate-100 px-2 py-1 text-xs leading-normal text-blue-700 dark:bg-[#2a3a4f]/70 dark:text-[#d8e2ff]"
                          key={citation}
                        >
                          {citation}
                        </span>
                      ))}
                    </div>
                  )}
                </article>
              ))}
            </div>

            <form
              className="mx-auto mb-4 grid w-[calc(100%-32px)] max-w-[800px] grid-cols-[40px_minmax(0,1fr)_40px] items-end gap-2 rounded-2xl border border-slate-300 bg-white p-2.5 shadow-[0_12px_30px_rgba(15,23,42,0.10)] transition focus-within:border-blue-500 focus-within:shadow-[0_0_0_3px_rgba(59,130,246,0.22),0_12px_30px_rgba(15,23,42,0.10)] dark:border-[#1e293b] dark:bg-[#0b1c30] dark:shadow-[0_12px_30px_rgba(0,0,0,0.16)] sm:mb-6 sm:w-[calc(100%-48px)]"
              onSubmit={handleSubmit}
            >
              <button
                className="inline-grid size-10 place-items-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-blue-600 dark:text-[#c2c6d6] dark:hover:bg-[#102034] dark:hover:text-[#adc6ff]"
                type="button"
                aria-label="Attach source"
              >
                <Icon name="paperclip" className="size-[18px]" />
              </button>
              <label className="sr-only" htmlFor="prompt">
                Ask a question
              </label>
              <textarea
                id="prompt"
                rows="1"
                value={prompt}
                onChange={(event) => setPrompt(event.target.value)}
                className="max-h-36 min-h-10 resize-none border-0 bg-transparent text-sm leading-normal text-slate-950 outline-0 placeholder:text-slate-500 dark:text-[#d3e4fe] dark:placeholder:text-[#c2c6d6]"
                placeholder="Ask about architecture, sources, citations, or retrieval traces..."
              />
              <button
                className="inline-grid size-10 place-items-center rounded-lg bg-blue-500 text-white transition hover:bg-blue-600 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400 dark:disabled:bg-[#1b2b3f] dark:disabled:text-[#8c909f]"
                type="submit"
                disabled={!canSend}
                aria-label="Send query"
              >
                <Icon name="send" className="size-[18px]" />
              </button>
            </form>
          </section>

          <aside
            className="flex min-w-0 flex-col gap-6 border-t border-slate-200 bg-white px-4 py-6 dark:border-[#424754] dark:bg-[#000f21] sm:px-6 lg:border-l lg:border-t-0"
            aria-label="Retrieval details"
          >
            <section>
              <p className="mb-3 text-xs font-medium uppercase leading-normal text-slate-500 dark:text-[#bec6e0]">
                Retrieval trace
              </p>
              <ol className="grid gap-2.5">
                {traces.map(([step, detail]) => (
                  <li
                    className="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:border-[#424754] dark:bg-[#0b1c30]"
                    key={step}
                  >
                    <span className="mb-1 block text-sm font-semibold capitalize leading-snug text-slate-950 dark:text-[#d3e4fe]">
                      {step}
                    </span>
                    <p className="m-0 text-sm leading-normal text-slate-500 dark:text-[#c2c6d6]">{detail}</p>
                  </li>
                ))}
              </ol>
            </section>

            <section>
              <p className="mb-3 text-xs font-medium uppercase leading-normal text-slate-500 dark:text-[#bec6e0]">
                Evidence
              </p>
              <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:border-[#424754] dark:bg-[#0b1c30]">
                <strong className="mb-1 block text-sm font-semibold leading-snug text-slate-950 dark:text-[#d3e4fe]">
                  Confidence: high
                </strong>
                <p className="m-0 text-sm leading-normal text-slate-500 dark:text-[#c2c6d6]">
                  Local plan excerpts support the generated answer and response shape.
                </p>
              </div>
            </section>
          </aside>
        </div>
      </section>
    </main>
  )
}

function Icon({ name, className = '' }) {
  const icons = {
    plus: (
      <>
        <path d="M12 5v14" />
        <path d="M5 12h14" />
      </>
    ),
    paperclip: (
      <>
        <path d="m21.4 11.6-8.5 8.5a6 6 0 0 1-8.5-8.5l8.5-8.5a4 4 0 0 1 5.7 5.7l-8.5 8.5a2 2 0 0 1-2.8-2.8l7.8-7.8" />
      </>
    ),
    send: (
      <>
        <path d="m22 2-7 20-4-9-9-4Z" />
        <path d="M22 2 11 13" />
      </>
    ),
    moon: (
      <path d="M20.99 12.62A8.5 8.5 0 1 1 11.38 3.01a6.5 6.5 0 0 0 9.61 9.61Z" />
    ),
    sun: (
      <>
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2" />
        <path d="M12 20v2" />
        <path d="m4.93 4.93 1.41 1.41" />
        <path d="m17.66 17.66 1.41 1.41" />
        <path d="M2 12h2" />
        <path d="M20 12h2" />
        <path d="m6.34 17.66-1.41 1.41" />
        <path d="m19.07 4.93-1.41 1.41" />
      </>
    ),
  }

  return (
    <svg
      className={`fill-none stroke-current stroke-2 [stroke-linecap:round] [stroke-linejoin:round] ${className}`}
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      {icons[name]}
    </svg>
  )
}

export default App
