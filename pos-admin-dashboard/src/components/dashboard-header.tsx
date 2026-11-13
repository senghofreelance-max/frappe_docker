"use client";

import { useState } from "react";
import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext";

export function DashboardHeader() {
  const [search, setSearch] = useState("");

  return <header className="dashboard-header">
    <div className="mobile-brand"><span className="brand-icon"><i className="pi pi-shop" aria-hidden="true" /></span><strong>CamPOS</strong></div>
    <label className="global-search"><i className="pi pi-search" aria-hidden="true" /><InputText aria-label="Search dashboard" placeholder="Search anything..." value={search} onChange={(event) => setSearch(event.target.value)} /><kbd>⌘ K</kbd></label>
    <div className="header-actions"><Button icon="pi pi-bell" aria-label="Notifications" text rounded className="bell-button" /><span className="header-divider" /><span className="admin-name"><strong>Sokha Retail</strong><small>Store admin</small></span><span className="avatar">SR</span></div>
  </header>;
}
