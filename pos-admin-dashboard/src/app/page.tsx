import { DashboardHeader } from "@/components/dashboard-header";
import { OrdersTable } from "@/components/orders-table";
import { SalesChart } from "@/components/sales-chart";

const menu = [["Overview", "pi pi-th-large"], ["Orders", "pi pi-shopping-bag"], ["Products", "pi pi-box"], ["Customers", "pi pi-users"], ["Reports", "pi pi-chart-bar"]];
const stats = [
  { title: "Total sales", value: "$24,780.50", change: "+12.8%", icon: "pi pi-wallet", color: "mint" },
  { title: "Total orders", value: "1,284", change: "+8.2%", icon: "pi pi-shopping-cart", color: "blue" },
  { title: "Products sold", value: "3,642", change: "+5.4%", icon: "pi pi-box", color: "amber" },
  { title: "New customers", value: "284", change: "+10.1%", icon: "pi pi-user-plus", color: "violet" },
];
const categories = [
  { name: "Groceries", share: "42%", total: "$10,407", color: "#3a8a68" },
  { name: "Beverages", share: "28%", total: "$6,938", color: "#75b594" },
  { name: "Household", share: "18%", total: "$4,460", color: "#c4a66d" },
  { name: "Other", share: "12%", total: "$2,975", color: "#d8e1dc" },
];
const products = [
  { name: "Cambo Coffee Blend", group: "Beverages", sold: "462 sold", total: "$4,620", initials: "CB", color: "#dfede5" },
  { name: "Palm Sugar 500g", group: "Groceries", sold: "318 sold", total: "$2,226", initials: "PS", color: "#f8ead6" },
  { name: "Angkor Rice 5kg", group: "Groceries", sold: "276 sold", total: "$1,932", initials: "AR", color: "#e6e8fb" },
];

export default function Home() {
  return (
    <div className="dashboard-root">
      <aside className="sidebar">
        <a href="#overview" className="brand"><span className="brand-icon"><i className="pi pi-shop" aria-hidden="true" /></span><span><strong>CamPOS</strong><small>Retail management</small></span></a>
        <p className="side-label">WORKSPACE</p>
        <nav aria-label="Main navigation">{menu.map(([name, icon], index) => <a key={name} href={`#${name.toLowerCase()}`} className={`nav-link ${index === 0 ? "active" : ""}`}><i className={icon} aria-hidden="true" />{name}{name === "Orders" && <span className="nav-count">8</span>}</a>)}</nav>
        <p className="side-label manage-label">MANAGE</p>
        <nav aria-label="Store management"><a href="#team" className="nav-link"><i className="pi pi-id-card" />Team members</a><a href="#settings" className="nav-link"><i className="pi pi-cog" />Settings</a></nav>
        <div className="store-status"><span className="open-dot" />Store is open<p>Phnom Penh · Central Market</p><a href="#store">View store <i className="pi pi-arrow-up-right" /></a></div>
        <div className="sidebar-user"><span className="avatar avatar-light">SR</span><span><strong>Sokha Retail</strong><small>Administrator</small></span></div>
      </aside>
      <main className="dashboard-main" id="overview">
        <DashboardHeader />
        <div className="page-content">
          <div className="page-heading"><div><p className="eyebrow">STORE OVERVIEW</p><h1>Good morning, Sokha <span aria-hidden="true">☀️</span></h1><p className="muted">Here&apos;s what&apos;s happening at your store today.</p></div><button className="export-button"><i className="pi pi-download" aria-hidden="true" /> Export report</button></div>
          <section className="stats-grid" aria-label="Store performance">{stats.map((item) => <article className="stat-card" key={item.title}><div className="stat-top"><span>{item.title}</span><span className={`stat-icon ${item.color}`}><i className={item.icon} aria-hidden="true" /></span></div><div className="stat-total"><strong>{item.value}</strong><span><i className="pi pi-arrow-up-right" aria-hidden="true" />{item.change}</span></div><p>Compared to last month</p></article>)}</section>
          <section className="content-grid"><SalesChart /><article className="panel-card"><div className="panel-heading"><div><h2>Sales by category</h2><p>Revenue contribution</p></div><button className="more-button" aria-label="Category options"><i className="pi pi-ellipsis-h" /></button></div><div className="donut-wrap"><div className="donut"><div><strong>$24.8k</strong><small>Total sales</small></div></div></div><div className="category-list">{categories.map((category) => <div className="category-row" key={category.name}><span className="category-dot" style={{ background: category.color }} /><span className="category-name">{category.name}</span><span className="category-share">{category.share}</span><strong>{category.total}</strong></div>)}</div></article></section>
          <section className="content-grid"><OrdersTable /><article id="products" className="panel-card"><div className="panel-heading"><div><h2>Top products</h2><p>Best sellers this month</p></div><a className="text-link" href="#products">See all</a></div><div className="product-list">{products.map((item, index) => <div className="product-row" key={item.name}><span className="product-thumb" style={{ background: item.color }}>{item.initials}</span><span className="product-info"><strong>{item.name}</strong><small>{item.group} · {item.sold}</small></span><span className="product-total"><strong>{item.total}</strong><small>#{index + 1} product</small></span></div>)}</div><a className="product-link" href="#products">View product insights <i className="pi pi-arrow-right" /></a></article></section>
          <footer className="dashboard-footer"><span>CamPOS Admin · Demo data · Frappe <code>{process.env.NEXT_PUBLIC_FRAPPE_URL ?? "http://localhost:8000"}</code></span><span>Last updated just now <i className="pi pi-refresh" /></span></footer>
        </div>
      </main>
    </div>
  );
}
