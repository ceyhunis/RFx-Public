import { Table } from "antd";
import { ColumnGroupType, ColumnsType } from "antd/es/table";
import React from "react";

export default function AntTable({
  columns,
  dataSource,
  title,
  style,
  onRow,
  isLoading,
  rowSelection,
}: {
  columns?: any[];
  dataSource: any[];
  title?: any;
  style?: React.CSSProperties;
  onRow?: any;
  isLoading?: boolean;
  rowSelection?: any;
}) {
  return (
    <Table
      loading={isLoading ?? false}
      title={title}
      size="small"
      virtual
      scroll={{ y: 600 }}
      style={style ?? { width: "100%", marginTop: "40px" }}
      columns={columns}
      dataSource={dataSource}
      pagination={false}
      bordered={false}
      onRow={onRow}
      rowClassName={"custom-table-row"}
      rowSelection={rowSelection}
  
    ></Table>
  );
}
