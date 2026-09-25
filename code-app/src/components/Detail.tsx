import { useState } from 'react';
import { saveReview } from '../dataverse';
import {
  AUDIENCE_LABELS,
  CAPABILITY_LABELS,
  CHANNEL_LABELS,
  CREDIT_COLORS,
  CREDIT_LABELS,
  DATA_SOURCE_LABELS,
  FREQUENCY_LABELS,
  LEVEL_LABELS,
  LICENCE_LABELS,
  PREDICTABILITY_LABELS,
  SENSITIVITY_LABELS,
  STATUS_LABELS,
  STATUS_OPTIONS,
  SYSTEM_ACCESS_LABELS,
  SYSTEM_TYPE_LABELS,
  TOOL_LABELS,
  TOOL_OPTIONS,
  URGENCY_LABELS,
  USERS_BAND_LABELS,
  YES_NO_UNKNOWN_LABELS,
  Status,
  labelFor,
  labelsFor,
  type AppConfig,
  type UseCaseRecord,
} from '../domain';
import { CreditPill, Empty, Fact, Info, StatusPill, Tags, ToolBadge } from './Shared';
import { creditWidth, formatDate, formatNumber } from './viewUtils';

function Recommendation({ record, config }: { record: UseCaseRecord; config: AppConfig }) {
  return (
    <section className="panel rec">
      <div className="head">
        <h3>Recommendation</h3>
        <ToolBadge tool={record.recommendedTool} />
      </div>
      <Fact label="Alternative" value={labelFor(TOOL_LABELS, record.alternativeTool)} />
      <Info label="Why this tool" value={record.rationale} />
      <div className="meter">
        <span>Credit band</span>
        <b>{labelFor(CREDIT_LABELS, record.creditBand)}</b>
        <i>
          <b
            style={{
              width: creditWidth(record.creditBand),
              background: record.creditBand === null ? '#737373' : CREDIT_COLORS[record.creditBand],
            }}
          />
        </i>
      </div>
      <div className="facts">
        <Fact label="Monthly credits" value={formatNumber(record.estimatedMonthlyCredits)} />
        <Fact label="Complexity" value={labelFor(LEVEL_LABELS, record.complexity)} />
        <Fact label="Confidence" value={labelFor(LEVEL_LABELS, record.confidence)} />
        <Fact label="Value" value={formatNumber(record.valueScore)} />
        <Fact label="Feasibility" value={formatNumber(record.feasibilityScore)} />
        <Fact label="Priority" value={formatNumber(record.priorityScore)} />
        <Fact label="Rubric" value={record.rubricVersion ?? 'Not set'} />
      </div>
      <Info label="Credit drivers" value={record.creditDrivers} />
      <Info label="Assumptions and open questions" value={record.assumptions} />
      <div className="links">
        <a href={config.toolGuideUrl} target="_blank" rel="noreferrer">
          Which agentic tool?
        </a>
        <a href={config.creditsGuideUrl} target="_blank" rel="noreferrer">
          Credits guide
        </a>
      </div>
    </section>
  );
}

function Systems({ record }: { record: UseCaseRecord }) {
  return (
    <section className="panel">
      <h3>Target systems</h3>
      {record.systems.length ? (
        <div className="systems">
          {record.systems.map((system) => (
            <article key={system.id}>
              <b>{system.name}</b>
              <span>{labelFor(SYSTEM_TYPE_LABELS, system.type)}</span>
              <span>
                {labelFor(SYSTEM_ACCESS_LABELS, system.access)} · Connector:{' '}
                {labelFor(YES_NO_UNKNOWN_LABELS, system.connectorAvailable)}
              </span>
            </article>
          ))}
        </div>
      ) : (
        <Empty title="No target systems listed" />
      )}
    </section>
  );
}

function Review({
  record,
  reviewerEmail,
  saved,
}: {
  record: UseCaseRecord;
  reviewerEmail: string;
  saved: () => Promise<void>;
}) {
  const [status, setStatus] = useState<number>(record.status ?? Status.InReview);
  const [finalTool, setFinalTool] = useState<number>(
    record.finalTool ?? record.recommendedTool ?? TOOL_OPTIONS[0],
  );
  const [notes, setNotes] = useState(record.reviewerNotes ?? '');
  const [info, setInfo] = useState(record.infoNeeded ?? '');
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function submit() {
    setBusy(true);
    setMessage(null);
    try {
      await saveReview(record, { status, finalTool, reviewerNotes: notes, infoNeeded: info, reviewerEmail });
      await saved();
      setMessage('Saved review changes.');
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Could not save review changes.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="panel review">
      <h3>Review panel</h3>
      <div className="formGrid">
        <label>
          <span>Status</span>
          <select value={status} onChange={(event) => setStatus(Number(event.target.value))}>
            {STATUS_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {STATUS_LABELS[option]}
              </option>
            ))}
          </select>
        </label>
        <label>
          <span>Final tool</span>
          <select value={finalTool} onChange={(event) => setFinalTool(Number(event.target.value))}>
            {TOOL_OPTIONS.map((option) => (
              <option key={option} value={option}>
                {TOOL_LABELS[option]}
              </option>
            ))}
          </select>
        </label>
      </div>
      <label>
        <span>Reviewer notes</span>
        <textarea rows={4} value={notes} onChange={(event) => setNotes(event.target.value)} />
      </label>
      <label>
        <span>Information needed</span>
        <textarea rows={3} value={info} onChange={(event) => setInfo(event.target.value)} />
      </label>
      <p className="muted">
        Saving stamps reviewed by {reviewerEmail || 'the current user'}. Approved or declined decisions also
        stamp today.
      </p>
      <button className="btn primary" type="button" disabled={busy} onClick={() => void submit()}>
        {busy ? 'Saving…' : 'Save review'}
      </button>
      {message ? <p className="formMsg">{message}</p> : null}
    </section>
  );
}

export function Detail({
  record,
  config,
  reviewerEmail,
  canReview,
  back,
  saved,
}: {
  record: UseCaseRecord;
  config: AppConfig;
  reviewerEmail: string;
  canReview: boolean;
  back: () => void;
  saved: () => Promise<void>;
}) {
  return (
    <div className="stack">
      <button className="btn ghost" type="button" onClick={back}>
        ← Back
      </button>
      <section className="panel detailHero">
        <div>
          <p className="eyebrow">{record.number ?? 'Use case'}</p>
          <h2>{record.title}</h2>
          <p className="muted">
            Submitted by {record.submitterEmail || 'unknown'} · {formatDate(record.createdOn)}
          </p>
        </div>
        <div className="badges">
          <StatusPill status={record.status} />
          <ToolBadge tool={record.finalTool ?? record.recommendedTool} />
          <CreditPill credit={record.creditBand} />
        </div>
      </section>

      <div className="detailGrid">
        <section className="panel">
          <h3>The idea in plain language</h3>
          <Info label="Problem to solve" value={record.problemStatement} />
          <Info label="Desired outcome" value={record.desiredOutcome} />
          <Info label="Current process" value={record.currentProcess} />
          <Info label="Example request or trigger" value={record.exampleRequest} />
          <Info label="Conversation summary" value={record.conversationSummary} />
        </section>

        <section className="panel">
          <h3>Profile</h3>
          <div className="facts">
            <Fact label="Audience" value={labelFor(AUDIENCE_LABELS, record.audience)} />
            <Fact label="Users" value={labelFor(USERS_BAND_LABELS, record.usersBand)} />
            <Fact label="Frequency" value={labelFor(FREQUENCY_LABELS, record.usageFrequency)} />
            <Fact label="Channel" value={labelFor(CHANNEL_LABELS, record.usageChannel)} />
            <Fact label="M365 Copilot" value={labelFor(LICENCE_LABELS, record.copilotLicence)} />
            <Fact label="Sensitivity" value={labelFor(SENSITIVITY_LABELS, record.sensitivity)} />
            <Fact label="Urgency" value={labelFor(URGENCY_LABELS, record.urgency)} />
            <Fact label="Predictability" value={labelFor(PREDICTABILITY_LABELS, record.predictability)} />
            <Fact
              label="Document heavy"
              value={record.documentHeavy === null ? 'Not set' : record.documentHeavy ? 'Yes' : 'No'}
            />
            <Fact label="Hours saved / month" value={formatNumber(record.hoursSavedPerMonth)} />
          </div>
          <Tags title="Data sources" tags={labelsFor(DATA_SOURCE_LABELS, record.dataSources)} />
          <Tags title="Capabilities" tags={labelsFor(CAPABILITY_LABELS, record.capabilities)} />
        </section>

        <Recommendation record={record} config={config} />
        <Systems record={record} />
        {!canReview && record.infoNeeded ? (
          <section className="panel warning">
            <h3>Information requested</h3>
            <p>{record.infoNeeded}</p>
          </section>
        ) : null}
        {canReview ? <Review record={record} reviewerEmail={reviewerEmail} saved={saved} /> : null}
      </div>
    </div>
  );
}
