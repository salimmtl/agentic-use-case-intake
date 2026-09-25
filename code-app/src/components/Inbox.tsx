import { useMemo, useState } from 'react';
import { Empty, Filter, UseCaseList } from './Shared';
import type { FilterValue } from './viewUtils';
import {
  AUDIENCE_LABELS,
  AUDIENCE_OPTIONS,
  CREDIT_LABELS,
  CREDIT_OPTIONS,
  STATUS_LABELS,
  STATUS_OPTIONS,
  TOOL_LABELS,
  TOOL_OPTIONS,
  type UseCaseRecord,
} from '../domain';

export function Inbox({
  records,
  open,
}: {
  records: UseCaseRecord[];
  open: (record: UseCaseRecord) => void;
}) {
  const [query, setQuery] = useState('');
  const [status, setStatus] = useState<FilterValue>('all');
  const [tool, setTool] = useState<FilterValue>('all');
  const [credit, setCredit] = useState<FilterValue>('all');
  const [audience, setAudience] = useState<FilterValue>('all');

  const filtered = useMemo(
    () =>
      records
        .filter(
          (record) =>
            !query.trim() ||
            [record.title, record.number ?? '', record.submitterEmail, record.problemStatement ?? '']
              .join(' ')
              .toLowerCase()
              .includes(query.toLowerCase()),
        )
        .filter((record) => status === 'all' || record.status === status)
        .filter((record) => tool === 'all' || record.recommendedTool === tool)
        .filter((record) => credit === 'all' || record.creditBand === credit)
        .filter((record) => audience === 'all' || record.audience === audience)
        .sort((a, b) => (b.createdOn ?? '').localeCompare(a.createdOn ?? '')),
    [audience, credit, query, records, status, tool],
  );

  const filtersActive =
    query.trim() !== '' || status !== 'all' || tool !== 'all' || credit !== 'all' || audience !== 'all';
  const clearFilters = () => {
    setQuery('');
    setStatus('all');
    setTool('all');
    setCredit('all');
    setAudience('all');
  };

  return (
    <section className="panel">
      <h2>Inbox</h2>
      <p className="muted">Search and filter every submitted idea.</p>
      <div className="filters">
        <label>
          <span>Search</span>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Title, ID, submitter or keyword"
          />
        </label>
        <Filter
          label="Status"
          value={status}
          options={STATUS_OPTIONS}
          labels={STATUS_LABELS}
          change={setStatus}
        />
        <Filter label="Tool" value={tool} options={TOOL_OPTIONS} labels={TOOL_LABELS} change={setTool} />
        <Filter
          label="Credit"
          value={credit}
          options={CREDIT_OPTIONS}
          labels={CREDIT_LABELS}
          change={setCredit}
        />
        <Filter
          label="Audience"
          value={audience}
          options={AUDIENCE_OPTIONS}
          labels={AUDIENCE_LABELS}
          change={setAudience}
        />
      </div>
      <div className="listToolbar">
        <span className="muted">
          Showing <b>{filtered.length}</b> of {records.length} ideas
        </span>
        {filtersActive ? (
          <button className="btn ghost" type="button" onClick={clearFilters}>
            Clear filters
          </button>
        ) : null}
      </div>
      {filtered.length ? (
        <UseCaseList records={filtered} open={open} />
      ) : (
        <Empty title="No matching ideas" hint="Try clearing a filter." />
      )}
    </section>
  );
}
