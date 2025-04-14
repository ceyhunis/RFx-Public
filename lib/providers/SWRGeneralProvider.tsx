"use client";

import { signOut, useSession } from "next-auth/react";
import React from "react";
import { SWRConfig } from "swr";

export default function SWRGeneralProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { data: session } = useSession();
  return (
    <SWRConfig
      value={{
        fetcher: (url) =>
          fetch(url, {
            headers: { Authorization: `Bearer ${session?.user?.accessToken}` },
          }).then(async (r) => {
            if (!r.ok) {
              if (r.status === 401) {
                signOut();
              }
              throw new Error(r.statusText);
            }
            return r.json();
          }),
      }}
    >
      {children}
    </SWRConfig>
  );
}
