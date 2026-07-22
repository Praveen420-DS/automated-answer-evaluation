export const formatDate = value => value ? new Intl.DateTimeFormat().format(new Date(value)) : '—';
