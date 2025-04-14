import AntTable from "@/components/AntDesign/AntTable";
import React, { useState } from "react";

export default function WrapperTable({
  data,
  title,
  columns,
  onRow,
  isLoading,
  height,
  rowSelection,
}: {
  data: any[];
  title?: any;
  columns?: any[];
  onRow?: any;
  isLoading?: boolean;
  height?: string;
  rowSelection?: any;
}) {
  const processedData = React.useMemo(() => {
    if (!Array.isArray(data)) {
      console.warn("Table data is not an array:", data);
      return [];
    }

    return data.map((item: any) => ({
      ...item,
      key: item.id || Math.random(),
    }));
  }, [data]);

  const processedColumns = columns
    ? columns
    : Object.keys(data[0]).map((key) => ({
        title: key,
        dataIndex: key,
        key: key,
      }));

  return (
    <AntTable
      rowSelection={rowSelection}
      isLoading={isLoading}
      onRow={onRow}
      style={{
        width: "100%",
        marginTop: 0,
        height: height ?? "92vh",
      }}
      dataSource={processedData}
      title={title}
      columns={processedColumns}
    />
  );
}
