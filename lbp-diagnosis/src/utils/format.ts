export function formatDate(isoString: string): string {
  if (!isoString) return ""

  const date = new Date(isoString)

  const d = date.getDate().toString().padStart(2, "0")
  const m = (date.getMonth() + 1).toString().padStart(2, "0")
  const y = date.getFullYear()

  const h = date.getHours().toString().padStart(2, "0")
  const min = date.getMinutes().toString().padStart(2, "0")

  return `${d}/${m}/${y} ${h}:${min}`
}
