import { Cards, Empty } from './Shared';
import type { AppConfig, UseCaseRecord } from '../domain';

export function Submitter({
  records,
  config,
  email,
  open,
}: {
  records: UseCaseRecord[];
  config: AppConfig;
  email: string;
  open: (record: UseCaseRecord) => void;
}) {
  const mine = records
    .filter((record) => email && record.submitterEmail.toLowerCase() === email.toLowerCase())
    .sort((a, b) => (b.createdOn ?? '').localeCompare(a.createdOn ?? ''));

  return (
    <div className="stack">
      <section className="hero submitHero">
        <div>
          <p className="eyebrow">Submit an idea</p>
          <h2>Have an idea for an agent?</h2>
          <p>Chat with our intake assistant — about 5 minutes.</p>
        </div>
        {config.intakeAgentUrl ? (
          <button
            className="btn primary"
            type="button"
            onClick={() => window.open(config.intakeAgentUrl, '_blank', 'noopener,noreferrer')}
          >
            Open intake assistant
          </button>
        ) : (
          <div className="adminNote">
            The intake assistant link is not configured yet. An admin must set sams_IntakeAgentUrl.
          </div>
        )}
      </section>
      <section className="panel">
        <h2>My submissions</h2>
        <p className="muted">Showing submissions for {email || 'the signed-in user'}.</p>
        {!email ? (
          <Empty
            title="We could not identify your email"
            hint="Open this app from Power Apps so it can read your signed-in profile."
          />
        ) : mine.length ? (
          <Cards records={mine} open={open} />
        ) : (
          <Empty
            title="No submissions found"
            hint="Ideas you submit through the assistant will appear here."
          />
        )}
      </section>
    </div>
  );
}
