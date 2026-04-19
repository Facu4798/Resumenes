
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Orbitron:wght@700;900&display=swap');

body {
  background: #0b0c10;
  color: #c5c6c7;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  line-height: 1.7;
  max-width: 820px;
  margin: 0 auto;
  padding: 40px 48px;
}

/* ── H1 ── */
h1 {
  text-align: center;
  font-family: 'Orbitron', monospace;
  font-size: 48px;
  font-weight: 900;
  color: #66fcf1;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0 0 1.4rem;
  padding-bottom: 0.5rem;
  position: relative;
  text-shadow: 0 0 8px #66fcf1aa, 0 0 24px #66fcf155, 0 0 48px #66fcf122;
  border-bottom: 2px solid #66fcf133;
}
h1::after {
  content: '';
  display: block;
  position: absolute;
  bottom: -2px; left: 0;
  width: 80vw; height: 2px;
  background: #66fcf1;
  box-shadow: 0 0 2px #66fcf1, 0 0 18px #66fcf199;
}

h1::before {
  content: '';
  display: block;
  position: absolute;
  bottom: 105%; left: 0;
  width: 80vw; height: 2px;
  background: #66fcf1;
  box-shadow: 0 0 2px #66fcf1, 0 0 18px #66fcf199;
}

/* ── H2 ── */
h2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: #c678dd;
  letter-spacing: 0.04em;
  margin: 2rem 0 0.8rem;
  padding-left: 14px;
  border-left: 3px solid #c678dd;
  text-shadow: 0 0 12px #c678dd66;
  position: relative;
}
h2::before {
  content: '##';
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: #c678dd55;
  position: absolute;
  left: -28px;
  top: 50%; transform: translateY(-50%);
}

/* ── H3 ── */
h3 {
  font-size: 1.05rem;
  font-weight: 600;
  color: #e5c07b;
  margin: 1.5rem 0 0.5rem;
  display: flex; align-items: center; gap: 10px;
  text-shadow: 0 0 10px #e5c07b55;
}
h3::before {
  content: '▸';
  color: #e5c07b;
  font-size: 0.8rem;
  text-shadow: 0 0 8px #e5c07b;
  animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { opacity: 1; text-shadow: 0 0 8px #e5c07b; }
  50%      { opacity: 0.4; text-shadow: none; }
}

/* ── H4 ── */
h4 {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  color: #98c379;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin: 1.2rem 0 0.4rem;
}

/* ── OL ── */
ol {
  padding-left: 1.6rem;
  margin: 0.8rem 0 1rem;
}
ol li {
  margin-bottom: 6px;
  padding-left: 6px;
  color: #c5c6c7;
}
ol li::marker {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  font-weight: 600;
  color: #66fcf1;
  text-shadow: 0 0 6px #66fcf188;
}

/* nested ol */
ol ol {
  margin: 4px 0 4px;
}
ol ol li::marker {
  color: #45a29e;
}
ol ol ol li::marker {
  color: #1f6b68;
}


/* ── TABLE ── */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.2rem 0;
  font-size: 0.9rem;
  border: 1px solid #1f2833;
  border-radius: 8px;
  overflow: hidden;
}
thead tr {
  background: #0d1f2d;
  border-bottom: 1px solid #66fcf133;
}
thead th {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 600;
  color: #66fcf1;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 10px 14px;
  text-align: left;
  text-shadow: 0 0 8px #66fcf155;
}
tbody tr {
  border-bottom: 1px solid #1a1f2e;
  transition: background 0.15s;
}
tbody tr:last-child { border-bottom: none; }
tbody tr:hover { background: #0d1420; }
tbody td { padding: 9px 14px; color: #c5c6c7; }
tbody tr:nth-child(even) td { background: #0a0e18; }
</style>

# Unidad 1: Introducción

## Subtema 1: Conceptos Fundamentales

### efejfrhkjl

# hello


