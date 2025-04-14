import { Input, Select } from "antd";

const { Option } = Select;

const SearchFilterBar = () => {
  return (
    <div style={{ 
      display: "flex", 
      gap: "8px", 
      marginBottom: "16px",
      width: "100%"
    }}>
      <Input 
        placeholder="Search RFX..." 
        style={{ 
          flex: 1,
          minWidth: "200px"
        }} 
      />
      <Select 
        defaultValue="All Status" 
        style={{ 
          width: "150px",
          minWidth: "150px"
        }}>
        <Option value="all">All Status</Option>
        <Option value="open">Open</Option>
        <Option value="closed">Closed</Option>
      </Select>
    </div>
  );
};

export default SearchFilterBar;