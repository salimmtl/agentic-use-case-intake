import { useCallback, useEffect, useState } from 'react';
import './App.css';
import { getSignedInEmail, loadAppConfig, loadWorkspace } from './dataverse';
import { IconMoon, IconRefresh, IconSun, MicrosoftLogo, MicrosoftWordmark } from './icons';
import { useTheme } from './theme';
import { Detail } from './components/Detail';
import { Inbox } from './components/Inbox';
import { Matrix } from './components/Matrix';
import { Overview } from './components/Overview';
import { Submitter } from './components/Submitter';
import type { AppConfig, UseCaseRecord } from './domain';

type Area = 'reviewer' | 'submitter';
type View = 'overview' | 'matrix' | 'inbox' | 'detail';

const EMPTY_CONFIG: AppConfig = { intakeAgentUrl: '', toolGuideUrl: '', creditsGuideUrl: '' };

export default function App() {
  const { theme, toggle } = useTheme();
  const [records, setRecords] = useState<UseCaseRecord[]>([]);
  const [config, setConfig] = useState<AppConfig>(EMPTY_CONFIG);
  const [email, setEmail] = useState('');
  const [area, setArea] = useState<Area>('reviewer');
  const [view, setView] = useState<View>('overview');
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setError(null);
    try {
      const [loadedRecords, loadedConfig, userEmail] = await Promise.all([
        loadWorkspace(),
        loadAppConfig(),
        getSignedInEmail(),
      ]);
      setRecords(loadedRecords);
      setConfig(loadedConfig);
      setEmail(userEmail);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong while loading Dataverse data.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void Promise.resolve().then(refresh);
  }, [refresh]);

  const selected = records.find((record) => record.id === selectedId) ?? null;

  function open(record: UseCaseRecord) {
    setSelectedId(record.id);
    setView('detail');
  }

  function switchArea(next: Area) {
    setArea(next);
    setView(next === 'reviewer' ? 'overview' : 'inbox');
    setSelectedId(null);
  }

  const main = loading ? (
    <div className="loading">
      <span className="spinner" />
      Loading use cases…
    </div>
  ) : error ? (
    <section className="panel error">
      <h2>Could not load the workspace</h2>
      <p>{error}</p>
      <button className="btn" type="button" onClick={() => void refresh()}>
        Try again
      </button>
    </section>
  ) : view === 'detail' && selected ? (
    <Detail
      record={selected}
      config={config}
      reviewerEmail={email}
      canReview={area === 'reviewer'}
      back={() => setView('inbox')}
      saved={refresh}
    />
  ) : area === 'submitter' ? (
    <Submitter records={records} config={config} email={email} open={open} />
  ) : view === 'matrix' ? (
    <Matrix records={records} open={open} />
  ) : view === 'inbox' ? (
    <Inbox records={records} open={open} />
  ) : (
    <Overview
      records={records}
      open={open}
      showMatrix={() => setView('matrix')}
      showInbox={() => setView('inbox')}
    />
  );

  return (
    <div className="app">
      <aside>
        <div className="brand">
          <span className="brand__mark">
            <MicrosoftLogo size={22} />
          </span>
          <div>
            <h1>Agentic Use Case Studio</h1>
            <p>Intake portfolio</p>
          </div>
        </div>
        <span className="brandrule" aria-hidden="true" />
        <nav>
          <button
            className={area === 'reviewer' ? 'nav active' : 'nav'}
            type="button"
            onClick={() => switchArea('reviewer')}
          >
            Reviewer workspace
          </button>
          <button
            className={area === 'submitter' ? 'nav active' : 'nav'}
            type="button"
            onClick={() => switchArea('submitter')}
          >
            Submit an idea
          </button>
        </nav>
        {area === 'reviewer' ? (
          <nav>
            <button
              className={view === 'overview' ? 'nav active' : 'nav'}
              type="button"
              onClick={() => setView('overview')}
            >
              Overview
            </button>
            <button
              className={view === 'matrix' ? 'nav active' : 'nav'}
              type="button"
              onClick={() => setView('matrix')}
            >
              Portfolio matrix
            </button>
            <button
              className={view === 'inbox' ? 'nav active' : 'nav'}
              type="button"
              onClick={() => setView('inbox')}
            >
              Inbox
            </button>
          </nav>
        ) : null}
        <button className="nav" type="button" onClick={() => void refresh()}>
          <IconRefresh size={16} />
          Refresh
        </button>
        <button className="nav" type="button" onClick={toggle}>
          {theme === 'dark' ? <IconSun size={16} /> : <IconMoon size={16} />}
          {theme === 'dark' ? 'Light theme' : 'Dark theme'}
        </button>
        <p className="signed">
          Signed in as
          <br />
          <b>{email || 'Power Apps user'}</b>
        </p>
        <MicrosoftWordmark />
      </aside>
      <main>{main}</main>
    </div>
  );
}
