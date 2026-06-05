/**
 * Coerce API / GraphQL skin metrics (0–100 scale) for charts and progress bars.
 */
export function toMetricPercent(value, decimals = 0) {
	const n = Number(value);
	if (!Number.isFinite(n)) return 0;
	const clamped = Math.min(100, Math.max(0, Math.abs(n)));
	return Number(clamped.toFixed(decimals));
}

export function toAgeYears(value) {
	const n = Number(value);
	if (!Number.isFinite(n)) return 0;
	return Math.min(100, Math.max(1, Math.round(Math.abs(n))));
}
