import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "DealSense AI — Investment Intelligence",
  description: "AI-powered due diligence for private equity and M&A teams."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}