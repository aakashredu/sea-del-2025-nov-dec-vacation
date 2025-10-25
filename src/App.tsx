import React, { useEffect, useRef, useState } from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

const STORAGE_KEY = 'aakash-preeti-india-2025-events'

function loadEvents() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw)
  } catch {
    return null
  }
}

function saveEvents(events:any[]) {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(events)) } catch {}
}

const initialEvents = [
  ...['2025-11-17','2025-11-18','2025-11-19','2025-11-20','2025-11-21'].map(d => ({
    id: `work-${d}`, title: 'Office: Delhi (No plans)', start: `${d}T10:00:00`, end: `${d}T18:30:00`,
  })),

  { id: '2025-11-22-brunch',  title: 'Chill + Local errands', start: '2025-11-22T11:00:00', end: '2025-11-22T13:00:00' },
  { id: '2025-11-22-outing',  title: 'India Gate/Kartavya Path evening walk', start: '2025-11-22T17:00:00', end: '2025-11-22T19:00:00' },
  { id: '2025-11-22-dinner',  title: 'Dinner: Kitchen District – Hyatt Centric, Janakpuri', start: '2025-11-22T20:00:00', end: '2025-11-22T22:00:00' },

  { id: '2025-11-23-vihaan-party', title: "Vihaan's Birthday @ Timezone, Pacific Mall (Party + Games)", start: '2025-11-23T16:00:00', end: '2025-11-23T19:00:00' },
  { id: '2025-11-23-dinner', title: "Family Dinner: Castle's Barbeque, Janakpuri", start: '2025-11-23T19:30:00', end: '2025-11-23T21:30:00' },

  ...['2025-11-24','2025-11-25','2025-11-26','2025-11-27','2025-11-28'].map(d => ({
    id: `work-${d}`, title: 'Office: Delhi (No plans)', start: `${d}T10:00:00`, end: `${d}T18:30:00`,
  })),

  { id: '2025-11-29-dhjp',  title: 'Dilli Haat Janakpuri (Crafts + Snacks)', start: '2025-11-29T16:30:00', end: '2025-11-29T18:30:00' },
  { id: '2025-11-29-rooftop',  title: 'Rooftop Dinner: Over The Top, Janakpuri', start: '2025-11-29T20:00:00', end: '2025-11-29T22:00:00' },
  { id: '2025-11-30-lodhi',  title: 'Lodhi Art District Walk + Lodhi Garden Picnic', start: '2025-11-30T11:00:00', end: '2025-11-30T14:00:00' },

  { id: '2025-12-03-drive-jaipur', title: 'Drive to Jaipur via NH48 (start early)', start: '2025-12-03T06:30:00', end: '2025-12-03T12:30:00' },
  { id: '2025-12-03-chowk', title: 'Jaipur: Hawa Mahal + Bapu Bazaar stroll', start: '2025-12-03T16:30:00', end: '2025-12-03T19:30:00' },
  { id: '2025-12-04-amber', title: 'Jaipur: Amber Fort & Jal Mahal', start: '2025-12-04T09:30:00', end: '2025-12-04T13:00:00' },
  { id: '2025-12-04-citypalace', title: 'City Palace + Jantar Mantar', start: '2025-12-04T15:00:00', end: '2025-12-04T18:00:00' },
  { id: '2025-12-05-pushkar', title: 'Day trip: Ajmer/Pushkar (Brahma Temple, lake)', start: '2025-12-05T09:30:00', end: '2025-12-05T18:30:00' },
  { id: '2025-12-06-return', title: 'Drive back to Delhi', start: '2025-12-06T07:00:00', end: '2025-12-06T13:00:00' },

  { id: '2025-12-07-family', title: 'Family Lunch (home/nearby)', start: '2025-12-07T13:00:00', end: '2025-12-07T15:00:00' },
  { id: '2025-12-10-dwarka', title: 'Dwarka: Vegas Mall dinner (Punjab Grill/Chili\'s)', start: '2025-12-10T20:00:00', end: '2025-12-10T22:00:00' },

  { id: '2025-12-12-dimpy', title: "Dimpy's Birthday Dinner: The Beer Café, Unity One Mall", start: '2025-12-12T20:00:00', end: '2025-12-12T23:00:00' },
  { id: '2025-12-14-old-delhi', title: 'Old Delhi Food Walk (Paranthe Wali Gali, Karim\'s)', start: '2025-12-14T17:00:00', end: '2025-12-14T20:30:00' },

  { id: '2025-12-19-depart', title: 'Fly DEL → SEA (Return)', start: '2025-12-19T21:00:00', end: '2025-12-19T23:59:00' },
]

export default function App() {
  const calendarRef = useRef<FullCalendar | null>(null)
  const [events, setEvents] = useState<any[]>(() => loadEvents() ?? initialEvents)
  const [view, setView] = useState<'dayGridMonth' | 'timeGridWeek' | 'timeGridDay'>('dayGridMonth')

  useEffect(() => { saveEvents(events) }, [events])

  const handleSelect = (sel:any) => {
    const title = prompt('Event title?')
    if (title) {
      const newEvent = { id: `ev-${Date.now()}`, title, start: sel.startStr, end: sel.endStr, allDay: sel.allDay }
      setEvents(prev => [...prev, newEvent])
    }
  }

  const handleEventClick = (info:any) => {
    const choice = window.prompt(`Edit title or type 'delete' to remove:\n\nCurrent: ${info.event.title}`, info.event.title)
    if (choice === null) return
    if (choice.toLowerCase() === 'delete') {
      setEvents(prev => prev.filter(e => e.id !== info.event.id))
    } else {
      setEvents(prev => prev.map(e => e.id === info.event.id ? { ...e, title: choice } : e))
    }
  }

  const persistEvent = (change:any) => {
    const { event } = change
    setEvents(prev => prev.map(e => e.id === event.id ? {
      ...e,
      start: event.start?.toISOString?.() ?? e.start,
      end: event.end?.toISOString?.() ?? e.end,
      allDay: event.allDay,
    } : e))
  }

  const handleReset = () => {
    if (confirm('Reset to the original itinerary? This will clear your changes.')) {
      setEvents(initialEvents)
    }
  }

  return (
    <div className="min-h-screen w-full bg-neutral-900 text-white p-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold">🇮🇳 Aakash & Preeti – India Trip Planner</h1>
            <p className="text-sm opacity-80">Nov 17 → Dec 19, 2025 · Your changes auto‑save to this device</p>
          </div>
          <div className="flex gap-2">
            <button onClick={() => setView('dayGridMonth')} className="px-3 py-1 rounded-xl bg-neutral-800 hover:bg-neutral-700">Month</button>
            <button onClick={() => setView('timeGridWeek')} className="px-3 py-1 rounded-xl bg-neutral-800 hover:bg-neutral-700">Week</button>
            <button onClick={() => setView('timeGridDay')} className="px-3 py-1 rounded-xl bg-neutral-800 hover:bg-neutral-700">Day</button>
            <button onClick={handleReset} className="px-3 py-1 rounded-xl bg-rose-600 hover:bg-rose-700">Reset</button>
          </div>
        </header>

        <div className="rounded-2xl overflow-hidden shadow-xl">
          <FullCalendar
            ref={calendarRef as any}
            plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
            initialView={view}
            headerToolbar={{ left: 'prev,next today', center: 'title', right: 'dayGridMonth,timeGridWeek,timeGridDay' }}
            height="auto"
            selectable
            selectMirror
            select={handleSelect}
            editable
            eventDrop={persistEvent}
            eventResize={persistEvent}
            eventClick={handleEventClick}
            events={events}
            firstDay={1}
            nowIndicator
            slotMinTime="07:00:00"
            slotMaxTime="23:00:00"
            initialDate="2025-11-17"
          />
        </div>

        <footer className="mt-6 text-xs opacity-70">
          <p>Tip: drag to create blocks; click an event to rename or type <em>delete</em> to remove. All edits persist in your browser (localStorage).</p>
        </footer>
      </div>
    </div>
  )
}
