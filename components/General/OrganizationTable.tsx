import React, { useState } from "react";
import { Spin, Table, Tag } from "antd";
import type { ColumnsType } from "antd/es/table";

interface Worker {
  key?: string;
  name: string;
  email: string;
  business_cycles?: string[];
}

interface OrganizationTableProps {
  data: Worker[] | any[];
  loading: boolean;
  error: Error | null;
}

const OrganizationTable: React.FC<OrganizationTableProps> = ({ data, loading, error }) => {
  const [selectedRowKeys, setSelectedRowKeys] = useState<string[]>([]);
  const [currentPage, setCurrentPage] = useState(1);

  const columns: ColumnsType<Worker> = [
    { title: "First Name", dataIndex: "first_name" },
    { title: "Last Name", dataIndex: "last_name" },
    { title: "Email", dataIndex: "email" },
    {
      title: "Business Cycles",
      dataIndex: "business_cycles",
      render: (business_cycles: string[] = []) => (
        <>
          {business_cycles.map((cycle) => (
            <Tag color="blue" key={cycle}>
              {cycle}
            </Tag>
          ))}
        </>
      ),
    },
  ];

  if (loading) return <Spin tip="Loading..." />;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <Table
      columns={columns}
      dataSource={data.map((item, index) => ({
        ...item,
        key: item.key || index.toString(),
      }))}
      style={{
        backgroundColor: "white",
        borderRadius: "16px",
        overflow: "hidden",
      }}
      pagination={{
        current: currentPage,
        pageSize: 5,
        total: data.length,
        onChange: setCurrentPage,
        showSizeChanger: false,
        showQuickJumper: false,
        showTotal: (total) => `Total ${total} items`,
        style: { marginTop: "16px" },
      }}
      rowSelection={{
        type: "checkbox",
        selectedRowKeys,
        onChange: (keys) => setSelectedRowKeys(keys as string[]),
        selections: [Table.SELECTION_ALL, Table.SELECTION_NONE],
      }}
      onRow={(record) => ({
        onClick: (e) => {
          if ((e.target as HTMLElement).tagName !== "INPUT") {
            const key = record.key as string;
            setSelectedRowKeys((prev) =>
              prev.includes(key)
                ? prev.filter((k) => k !== key)
                : [...prev, key]
            );
          }
        },
        style: { cursor: "pointer" },
      })}
    />
  );
};

export default OrganizationTable;
