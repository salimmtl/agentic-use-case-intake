import type { CSSProperties } from 'react';
import {
  CREDIT_COLORS,
  CREDIT_LABELS,
  STATUS_COLORS,
  STATUS_LABELS,
  TOOL_COLORS,
  TOOL_LABELS,
  labelFor,
  type UseCaseRecord,
} from '../domain';
import { formatDate, type FilterValue } from './viewUtils';

function chipStyle(color: string): CSSProperties {
  return { '--chip-color': color } as CSSProperties;
}

function Pill({ label, color, strong = false }: { label: string; color: string; strong?: boolean }) {
  return (
    <span className={strong ? 'pill pill--strong' : 'pill'} style={chipStyle(color)} title={label}>
      <span className="pill__text">{label}</span>
    </span>
  );
}

export function StatusPill({ status }: { status: number | null }) {
  return (
    <Pill
      label={labelFor(STATUS_LABELS, status)}
      color={status === null ? '#737373' : STATUS_COLORS[status]}
    />
  );
}

export function ToolBadge({ tool }: { tool: number | null }) {
  return (
    <Pill
      strong
      label={labelFor(TOOL_LABELS, tool, 'Recommendation pending')}
      color={tool === null ? '#737373' : TOOL_COLORS[tool]}
    />
  );
}

export function CreditPill({ credit }: { credit: number | null }) {
  return (
    <Pill
      label={labelFor(CREDIT_LABELS, credit)}
      color={credit === null ? '#737373' : CREDIT_COLORS[credit]}
    />
  );
}

export function Empty({ title, hint }: { title: string; hint?: string }) {
  return (
    <div className="empty">
      <p className="empty__title">{title}</p>
      {hint ? <p className="empty__hint">{hint}</p> : null}
    </div>
  );
}

export function Kpi({ label, value, hint }: { label: string; value: string | number; hint?: string }) {
  return (
    <article className="kpi">
      <p>{label}</p>
      <strong>{value}</strong>
      {hint ? <span>{hint}</span> : null}
    </article>
  );
}

export function Filter({
  label,
  value,
  options,
  labels,
  change,
}: {
  label: string;
  value: FilterValue;
  options: number[];
  labels: Record<number, string>;
  change: (value: FilterValue) => void;
}) {
  return (
    <label>
      <span>{label}</span>
      <select
        value={value}
        onChange={(event) => change(event.target.value === 'all' ? 'all' : Number(event.target.value))}
      >
        <option value="all">All</option>
        {options.map((option) => (
          <option key={option} value={option}>
            {labels[option]}
          </option>
        ))}
      </select>
    </label>
  );
}

export function UseCaseList({
  records,
  open,
}: {
  records: UseCaseRecord[];
  open: (record: UseCaseRecord) => void;
}) {
  return (
    <div className="ucList" role="table" aria-label="Agentic use cases">
      <div className="ucList__head" role="row">
        <span role="columnheader">ID</span>
        <span role="columnheader">Idea</span>
        <span role="columnheader">Status</span>
        <span role="columnheader">Recommended tool</span>
        <span role="columnheader">Credit band</span>
        <span role="columnheader">Submitted</span>
      </div>
      {records.map((record) => (
        <button
          key={record.id}
          className="ucRow"
          type="button"
          role="row"
          onClick={() => open(record)}
          aria-label={`Open ${record.number ?? 'new idea'}: ${record.title}`}
        >
          <span className="ucRow__id" role="cell">
            {record.number ?? 'New'}
          </span>
          <span className="ucRow__idea" role="cell">
            <strong title={record.title}>{record.title}</strong>
            <small title={record.submitterEmail}>{record.submitterEmail || 'Unknown submitter'}</small>
          </span>
          <span role="cell" data-label="Status">
            <StatusPill status={record.status} />
          </span>
          <span role="cell" data-label="Tool">
            <ToolBadge tool={record.recommendedTool} />
          </span>
          <span role="cell" data-label="Credit">
            <CreditPill credit={record.creditBand} />
          </span>
          <span className="ucRow__date" role="cell">
            {formatDate(record.createdOn)}
          </span>
        </button>
      ))}
    </div>
  );
}

export function Cards({
  records,
  open,
  compact = false,
}: {
  records: UseCaseRecord[];
  open: (record: UseCaseRecord) => void;
  compact?: boolean;
}) {
  return (
    <div className={compact ? 'cards compact' : 'cards'}>
      {records.map((record) => (
        <button key={record.id} className="card" type="button" onClick={() => open(record)}>
          <span className="cardTop">
            <b>{record.number ?? 'New idea'}</b>
            <StatusPill status={record.status} />
          </span>
          <strong>{record.title}</strong>
          <small>
            {record.submitterEmail || 'Unknown submitter'} · {formatDate(record.createdOn)}
          </small>
          <span className="badges">
            <ToolBadge tool={record.recommendedTool} />
            <CreditPill credit={record.creditBand} />
          </span>
        </button>
      ))}
    </div>
  );
}

export function Fact({ label, value }: { label: string; value: string }) {
  return (
    <span className="fact">
      <span>{label}</span>
      <b>{value}</b>
    </span>
  );
}

export function Info({ label, value }: { label: string; value: string | null }) {
  return (
    <div className="info">
      <h4>{label}</h4>
      <p>{value ?? 'Not provided yet.'}</p>
    </div>
  );
}

export function Tags({ title, tags }: { title: string; tags: string[] }) {
  return (
    <div className="tagGroup">
      <h4>{title}</h4>
      {tags.length ? (
        <div className="tags">
          {tags.map((tag) => (
            <span className="tag" key={tag}>
              {tag}
            </span>
          ))}
        </div>
      ) : (
        <p className="muted">Not specified.</p>
      )}
    </div>
  );
}
