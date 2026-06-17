"use client";

import { useEffect } from "react";
import { getHealth } from "@/lib/api";

export default function Home() {
  useEffect(() => {
    getHealth().then(console.log);
  }, []);

  return (
    <div>
      GitHub Intelligence Platform
    </div>
  );
}