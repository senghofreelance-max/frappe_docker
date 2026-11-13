"use client";

import { useState } from "react";
import { Button } from "primereact/button";
import { Column } from "primereact/column";
import { DataTable } from "primereact/datatable";
import { InputText } from "primereact/inputtext";
import { Tag } from "primereact/tag";

type Order = { id: string; customer: string; initials: string; date: string; amount: number; status: "Completed" | "Processing" | "Pending" };
const orders: Order[] = [
  { id: "#CP-10482", customer: "Dara Sopheak", initials: "DS", date: "Today, 10:42 AM", amount: 128.5, status: "Completed" },
  { id: "#CP-10481", customer: "Malis Chan", initials: "MC", date: "Today, 10:18 AM", amount: 86, status: "Processing" },
  { id: "#CP-10480", customer: "Vannak Kim", initials: "VK", date: "Today, 09:56 AM", amount: 245.75, status: "Completed" },
  { id: "#CP-10479", customer: "Sreymom Heng", initials: "SH", date: "Today, 09:31 AM", amount: 42.25, status: "Pending" },
  { id: "#CP-10478", customer: "Borey Lim", initials: "BL", date: "Today, 09:12 AM", amount: 310, status: "Completed" },
];
const statusSeverity: Record<Order["status"], "success" | "info" | "warning"> = { Completed: "success", Processing: "info", Pending: "warning" };

export function OrdersTable() {
  const [search, setSearch] = useState("");
  const query = search.trim().toLowerCase();
  const visibleOrders = query ? orders.filter((order) => `${order.id} ${order.customer} ${order.status}`.toLowerCase().includes(query)) : orders;
  const customerBody = (order: Order) => <div className="customer-cell"><span className="customer-avatar">{order.initials}</span>{order.customer}</div>;
  const statusBody = (order: Order) => <Tag value={order.status} severity={statusSeverity[order.status]} rounded />;

  return <article id="orders" className="panel-card orders-panel">
    <div className="panel-heading"><div><h2>Recent orders</h2><p>Track your latest transactions</p></div><a className="text-link" href="#orders">View all orders <i className="pi pi-arrow-right" /></a></div>
    <div className="table-toolbar"><label className="table-search"><i className="pi pi-search" aria-hidden="true" /><InputText value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search orders..." aria-label="Search orders" /></label><Button icon="pi pi-sliders-h" aria-label="Filter orders" outlined className="filter-button" /></div>
    <DataTable value={visibleOrders} dataKey="id" size="small" paginator rows={5} emptyMessage="No matching orders." className="orders-datatable" tableStyle={{ minWidth: "590px" }}>
      <Column field="id" header="ORDER ID" body={(order: Order) => <span className="order-id">{order.id}</span>} />
      <Column field="customer" header="CUSTOMER" body={customerBody} />
      <Column field="date" header="DATE" body={(order: Order) => <span className="date-cell">{order.date}</span>} />
      <Column field="amount" header="AMOUNT" body={(order: Order) => <strong>${order.amount.toFixed(2)}</strong>} />
      <Column field="status" header="STATUS" body={statusBody} />
    </DataTable>
  </article>;
}
