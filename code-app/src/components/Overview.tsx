import { Bars, Donut } from './Charts';
import { group, isRecent, lastSevenDays, trend } from './chartUtils';
import { Empty, Kpi, UseCaseList } from './Shared';
import {
  AUDIENCE_LABELS,
  CREDIT_COLORS,
  CREDIT_LABELS,
  CREDIT_OPTIONS,
  CreditBand,
  STATUS_COLORS,
  STATUS_LABELS,
  STATUS_OPTIONS,
  Status,
  TOOL_LABELS,
  labelFor,
  type UseCaseRecord,
} from '../domain';

export function Overview({
  records,
  open,
  showMatrix,
  showInbox,
}: {
  records: UseCaseRecord[];
  open: (record: UseCaseRecord) => void;
  showMatrix: () => void;
  showInbox: () => void;
}) {
  const statusData = STATUS_OPTIONS.map((status) => ({
    label: STATUS_LABELS[status],
    count: records.filter((record) => record.status === status).length,
    color: STATUS_COLORS[status],
  }));
  const creditData = CREDIT_OPTIONS.map((credit) => ({
    label: CREDIT_LABELS[credit],
    count: records.filter((record) => record.creditBand === credit).length,
    color: CREDIT_COLORS[credit],
  }));
  const systems = group(
    records.flatMap((record) => record.systems.map((system) => ({ ...record, title: system.name }))),
    (record) => record.title,
  );
  const recent = [...records]
    .sort((a, b) => (b.createdOn ?? '').localeCompare(a.createdOn ?? ''))
    .slice(0, 6);

  return (
    <div className="stack">
      <section className="hero">
        <div>
          <p className="eyebrow">Reviewer workspace</p>
          <h2>Understand what people are asking for and prioritize the right agentic work.</h2>
        </div>
        <button className="btn primary" type="button" onClick={showMatrix}>
          Open matrix
        </button>
      </section>

      <section className="kpis">
        <Kpi label="Total" value={records.length} />
        <Kpi
          label="New this week"
          value={records.filter((record) => isRecent(record.createdOn, lastSevenDays())).length}
        />
        <Kpi
          label="Awaiting review"
          value={
            records.filter(
              (record) => record.status === Status.Submitted || record.status === Status.InReview,
            ).length
          }
          hint="Submitted + in review"
        />
        <Kpi
          label="Needs info"
          value={records.filter((record) => record.status === Status.NeedsInfo).length}
        />
        <Kpi
          label="Approved / in build / live"
          value={
            records.filter((record) =>
              [Status.Approved, Status.InBuild, Status.Live].includes(record.status as never),
            ).length
          }
        />
        <Kpi
          label="High credit band"
          value={records.filter((record) => record.creditBand === CreditBand.High).length}
        />
      </section>

      <section className="grid">
        <Donut title="By status" data={statusData} />
        <Donut title="By credit band" data={creditData} />
        <Bars
          title="By recommended tool"
          data={group(records, (record) => labelFor(TOOL_LABELS, record.recommendedTool, 'Not assessed'))}
        />
        <Bars
          title="By audience"
          data={group(records, (record) => labelFor(AUDIENCE_LABELS, record.audience, 'Not specified'))}
        />
        <Bars title="Top target systems" data={systems} />
        <section className="panel chart">
          <h3>Submissions per week</h3>
          <div className="trend">
            {trend(records).map((week) => (
              <span key={week.label}>
                <i style={{ height: `${Math.max(8, week.pct)}%` }} title={`${week.label}: ${week.count}`} />
                <b>{week.label.split(' ')[0]}</b>
              </span>
            ))}
          </div>
        </section>
      </section>

      <section className="panel">
        <div className="panelHead">
          <h3>Newest ideas</h3>
          <button className="btn ghost" type="button" onClick={showInbox}>
            View all in inbox →
          </button>
        </div>
        {recent.length ? <UseCaseList records={recent} open={open} /> : <Empty title="No submissions yet" />}
      </section>
    </div>
  );
}
