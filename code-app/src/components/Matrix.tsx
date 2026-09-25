import { CREDIT_COLORS, type UseCaseRecord } from '../domain';
import { Empty } from './Shared';

const scoreTicks = [1, 2, 3, 4, 5];

export function Matrix({
  records,
  open,
}: {
  records: UseCaseRecord[];
  open: (record: UseCaseRecord) => void;
}) {
  const scored = records.filter((record) => record.valueScore !== null && record.feasibilityScore !== null);

  return (
    <section className="panel matrixPanel">
      <h2>Portfolio matrix</h2>
      <p className="muted">
        Value rises upward. Feasibility increases to the right. Colour shows credit band; size shows priority.
      </p>
      <div className="matrix">
        {scoreTicks.map((tick) => (
          <span key={`v${tick}`} className="gridLine v" style={{ left: `${tick * 20}%` }} />
        ))}
        {scoreTicks.map((tick) => (
          <span key={`h${tick}`} className="gridLine h" style={{ bottom: `${tick * 20}%` }} />
        ))}
        <b className="axis y">Value</b>
        <b className="axis x">Feasibility</b>
        {scored.map((record) => {
          const x = ((record.feasibilityScore ?? 1) - 0.5) * 20;
          const y = ((record.valueScore ?? 1) - 0.5) * 20;
          const size = 24 + Math.min(30, (record.priorityScore ?? 1) * 1.2);
          const color = record.creditBand === null ? '#737373' : CREDIT_COLORS[record.creditBand];
          return (
            <button
              key={record.id}
              className="bubble"
              type="button"
              style={{ left: `${x}%`, bottom: `${y}%`, width: size, height: size, background: color }}
              onClick={() => open(record)}
              title={`${record.title}: value ${record.valueScore}, feasibility ${record.feasibilityScore}`}
            >
              {record.priorityScore ?? ''}
            </button>
          );
        })}
      </div>
      {scored.length ? null : <Empty title="No scored ideas yet" />}
    </section>
  );
}
