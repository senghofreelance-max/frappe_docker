"use client";

import { PrimeReactProvider } from "primereact/api";
import type { PropsWithChildren } from "react";

export function PrimeProvider({ children }: PropsWithChildren) {
  return <PrimeReactProvider value={{ ripple: true }}>{children}</PrimeReactProvider>;
}
