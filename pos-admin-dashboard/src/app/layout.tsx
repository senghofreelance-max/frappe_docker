import type { Metadata } from "next";
import type { ReactNode } from "react";
import "primereact/resources/themes/lara-light-green/theme.css";
import "primeicons/primeicons.css";
import "./globals.css";
import { PrimeProvider } from "@/components/prime-provider";

export const metadata: Metadata = {
  title: "CamPOS Admin | Retail dashboard",
  description: "Point of sale and retail operations dashboard.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return <html lang="en" className="h-full antialiased"><body className="min-h-full"><PrimeProvider>{children}</PrimeProvider></body></html>;
}
