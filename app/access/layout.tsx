import AntLayout from "@/components/AntDesign/AntLayout";
import React, { ReactNode, Suspense } from "react";

export default function LayoutAccess({ children }: { children: ReactNode }) {
  return (
    <AntLayout>
      <Suspense>{children}</Suspense>
    </AntLayout>
  );
}
