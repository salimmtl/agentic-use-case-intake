import type { UseCaseRecord } from '../domain';

export function group(records: UseCaseRecord[], key: (record: UseCaseRecord) => string) {
  const map = new Map<string, number>();
  records.forEach((record) => map.set(key(record), (map.get(key(record)) ?? 0) + 1));
  return [...map]
    .map(([label, count]) => ({ label, count }))
    .sort((a, b) => b.count - a.count || a.label.localeCompare(b.label));
}

function todayMidnight(): Date {
  const date = new Date();
  date.setHours(0, 0, 0, 0);
  return date;
}

function addDays(date: Date, days: number): Date {
  const copy = new Date(date);
  copy.setDate(copy.getDate() + days);
  return copy;
}

export function currentTrendWindowStart(): Date {
  return addDays(todayMidnight(), -6);
}

export function isRecent(value: string | null, since: Date, until = new Date()): boolean {
  const date = value ? new Date(value) : null;
  return Boolean(date && !Number.isNaN(date.getTime()) && date >= since && date <= until);
}

export function lastSevenDays(): Date {
  return currentTrendWindowStart();
}

export function trend(records: UseCaseRecord[]) {
  const now = new Date();
  const start = addDays(todayMidnight(), -83);
  const buckets = Array.from({ length: 12 }, (_, index) => {
    const date = addDays(start, index * 7);
    const end = addDays(date, 7);
    return {
      date,
      end,
      label: date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }),
      count: 0,
    };
  });

  records.forEach((record) => {
    const created = record.createdOn ? new Date(record.createdOn) : null;
    if (!created || Number.isNaN(created.getTime()) || created < start || created > now) return;
    const bucket = buckets.find((candidate) => created >= candidate.date && created < candidate.end);
    if (bucket) bucket.count += 1;
  });

  const max = Math.max(1, ...buckets.map((bucket) => bucket.count));
  return buckets.map((bucket) => ({ ...bucket, pct: (bucket.count / max) * 100 }));
}
