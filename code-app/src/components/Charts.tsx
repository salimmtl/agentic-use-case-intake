import { Empty } from './Shared';
export function Bars({ title, data }: { title: string; data: { label: string; count: number }[] }) {
  const max = Math.max(1, ...data.map((item) => item.count));
  return (
    <section className="panel chart">
      <h3>{title}</h3>
      {data.length ? (
        <div className="bars">
          {data.slice(0, 8).map((item) => (
            <div className="bar" key={item.label}>
              <span>{item.label}</span>
              <i>
                <b style={{ width: `${Math.max(8, (item.count / max) * 100)}%` }} />
              </i>
              <strong>{item.count}</strong>
            </div>
          ))}
        </div>
      ) : (
        <Empty title="No data yet" />
      )}
    </section>
  );
}

export function Donut({
  title,
  data,
}: {
  title: string;
  data: { label: string; count: number; color: string }[];
}) {
  const total = data.reduce((sum, item) => sum + item.count, 0);
  const segments = data.map((item, index) => {
    const dash = total ? (item.count / total) * 100 : 0;
    const previousDash = data
      .slice(0, index)
      .reduce((sum, previous) => sum + (total ? (previous.count / total) * 100 : 0), 0);
    return { ...item, dash, offset: 25 - previousDash };
  });

  return (
    <section className="panel chart">
      <h3>{title}</h3>
      {total ? (
        <div className="donutWrap">
          <svg viewBox="0 0 42 42" className="donut" role="img" aria-label={title}>
            <circle className="donutBg" cx="21" cy="21" r="15.9" />
            {segments.map((segment) => (
              <circle
                key={segment.label}
                className="donutSeg"
                cx="21"
                cy="21"
                r="15.9"
                stroke={segment.color}
                strokeDasharray={`${segment.dash} ${100 - segment.dash}`}
                strokeDashoffset={segment.offset}
              />
            ))}
          </svg>
          <ul className="legend">
            {segments.map((segment) => (
              <li key={segment.label}>
                <i style={{ background: segment.color }} />
                {segment.label}
                <b>{segment.count}</b>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <Empty title="No data yet" />
      )}
    </section>
  );
}
