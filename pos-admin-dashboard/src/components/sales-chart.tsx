const bars = [34, 48, 42, 64, 53, 73, 60, 86, 71, 95, 67, 80];

export function SalesChart() {
  return <article className="panel-card">
    <div className="panel-heading"><div><h2>Sales overview</h2><p>Daily revenue performance</p></div><button className="period-select">This month <i className="pi pi-chevron-down" /></button></div>
    <div className="sales-total"><strong>$24,780.50</strong><span><i className="pi pi-arrow-up-right" /> 12.8%</span></div>
    <div className="chart-grid" aria-label="Sales chart showing daily revenue for November">{["$8k", "$6k", "$4k", "$2k"].map((tick, index) => <div className="chart-guide" key={tick} style={{ top: `${index * 29}%` }}><span>{tick}</span></div>)}{bars.map((height, index) => <div className="bar-column" key={index}><span className={`sales-bar ${index === 9 ? "sales-bar-highlight" : ""}`} style={{ height: `${height}%` }} /><small>{index * 2 + 1}</small></div>)}</div>
    <div className="chart-dates"><span>Nov 1</span><span>Nov 7</span><span>Nov 14</span><span>Nov 21</span><span>Nov 30</span></div>
  </article>;
}
