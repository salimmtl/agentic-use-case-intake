import { CreditBand } from '../domain';

export type FilterValue = number | 'all';

export function formatDate(value: string | null): string {
  const date = value ? new Date(value) : null;
  return date && !Number.isNaN(date.getTime())
    ? date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
    : '—';
}

export function formatNumber(value: number | null): string {
  return typeof value === 'number' ? value.toLocaleString() : '—';
}

export function creditWidth(credit: number | null) {
  if (credit === CreditBand.Included) return '18%';
  if (credit === CreditBand.Low) return '42%';
  if (credit === CreditBand.Medium) return '68%';
  if (credit === CreditBand.High) return '100%';
  return '8%';
}
