import AntContent from "@/components/AntDesign/AntContent";
import AntLayout from "@/components/AntDesign/AntLayout";
import GeneralSider from "@/components/General/DashboardSider";
import { DrawerContextProvider } from "@/lib/providers/DrawerContextProvider";

import { auth } from "@/auth";
import {
  AppstoreOutlined,
  ClusterOutlined,
  PartitionOutlined,
  ProductOutlined,
  ProfileOutlined,
  SettingOutlined,
  SolutionOutlined,
  TruckOutlined,
  UsergroupAddOutlined,
} from "@ant-design/icons";
import Link from "next/link";
import { redirect } from "next/navigation";
import React from "react";

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth();
  if (!session?.user?.id) {
    redirect("/");
  }

  const linkStyle = {
    fontSize: 12,
  };

  const items = [
    {
      key: "admin-2",
      label: (
        <Link style={linkStyle} href="/admin/role-management">
          Role Management
        </Link>
      ),
      href: "/admin/role-management",
      icon: (
        <UsergroupAddOutlined
          style={{
            color: "black",
          }}
        />
      ),
    },
    {
      key: "admin-6",
      label: (
        <Link style={linkStyle} href="/admin/organization-management">
          Organization Management
        </Link>
      ),
      href: "/admin/organization-management",
      icon: (
        <ClusterOutlined
          style={{
            color: "black",
          }}
        />
      ),
    },
    {
      key: "admin-3",
      label: (
        <Link style={linkStyle} href="/admin/user-management">
          User Management
        </Link>
      ),
      href: "/admin/user-management",
      icon: (
        <SettingOutlined
          style={{
            color: "black",
          }}
        />
      ),
    },
    {
      key: "admin-4",
      label: (
        <Link style={linkStyle} href="/admin/industry">
          Industry Management
        </Link>
      ),
      href: "/admin/industry",
      icon: (
        <AppstoreOutlined
          style={{
            color: "black",
          }}
        />
      ),
    },
    {
      key: "admin-5",
      label: (
        <Link style={linkStyle} href="/admin/service">
          Service/Item List Management
        </Link>
      ),
      href: "/admin/service",
      icon: (
        <ProfileOutlined
          style={{
            color: "black",
          }}
        />
      ),
    },

    {
      key: "admin-7",
      label: (
        <Link style={linkStyle} href="/admin/businesscycle">
          Business Cycle Management
        </Link>
      ),
      href: "/admin/businesscycle",
      icon: (
        <SolutionOutlined
          style={{
            color: "black",
          }}
        />
      ),
    },
    {
      key: "admin-8",
      label: (
        <Link style={linkStyle} href="/admin/funtional-area">
          Functional Area Management
        </Link>
      ),
      href: "/admin/funtional-area",
      icon: (
        <PartitionOutlined
          style={{
            color: "black",
          }}
        />
      ),
    },

    {
      key: "admin-11",
      label: (
        <Link style={linkStyle} href="/admin/provider-management">
          Provider Management
        </Link>
      ),
      href: "/admin/provider-management",
      icon: (
        <TruckOutlined
          style={{
            color: "black",
          }}
        />
      ),
    },
  ];

  return (
    <AntLayout>
      {" "}
      <DrawerContextProvider>
        <AntLayout hasSider>
          <GeneralSider items={items} />
          <AntContent style={{ padding: 0, margin: 0 }}>{children}</AntContent>
        </AntLayout>
      </DrawerContextProvider>
    </AntLayout>
  );
}
