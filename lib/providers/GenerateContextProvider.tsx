"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";

// Step 1: Define the context shape
interface GenerateContextType {
  name: string;
  description: string;
  company_url: string;
  value_propositions: string;
  industry: {
    id: number;
    name: string;
  };
  service_ids: Array<{
    id: number;
    name: string;
    description?: string;
  }>;
  business_cycle_ids: any[];
  functional_area_ids: any[];
  selectedFunctionalAreas: any[]; 
  start_date: string | null;
  end_date: string | null;
  setName: (name: string) => void;
  setDescription: (description: string) => void;
  setCompanyUrl: (url: string) => void;
  setValuePropositions: (value: string) => void;
  setIndustry: (industry: { id: number; name: string }) => void;
  setService_ids: (value: Array<{
    id: number;
    name: string;
    description?: string;
  }>) => void;
  setBusinessCycle_ids: (business_cycle_ids: any[]) => void;
  setFunctionalArea_ids: (functional_area_ids: any[]) => void;
  setSelectedFunctionalAreas: (functionalAreas: any[]) => void;
  setStartDate: (date: string | null) => void;
  setEndDate: (date: string | null) => void;
}

// Step 2: Create the context
const GenerateContext = createContext<GenerateContextType | undefined>(
  undefined
);

// Step 3: Implement the provider component
interface GenerateProviderProps {
  children: ReactNode;
}

export const GenerateProvider = ({ children }: GenerateProviderProps) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [company_url, setCompanyUrl] = useState("");
  const [value_propositions, setValuePropositions] = useState("");
  const [industry, setIndustry] = useState({ id: 0, name: "" });
  const [service_ids, setService_ids] = useState<Array<{
    id: number;
    name: string;
    description?: string;
  }>>([]);
  const [business_cycle_ids, setBusinessCycle_ids] = useState<any[]>([]);
  const [functional_area_ids, setFunctionalArea_ids] = useState<any[]>([]);
  const [selectedFunctionalAreas, setSelectedFunctionalAreas] = useState<any[]>(
    []
  );
  const [start_date, setStartDate] = useState<string | null>(null);
  const [end_date, setEndDate] = useState<string | null>(null);

  const value = {
    name,
    description,
    company_url,
    value_propositions,
    industry,
    service_ids,
    business_cycle_ids,
    functional_area_ids,
    selectedFunctionalAreas,
    start_date,
    end_date,
    setName,
    setDescription,
    setCompanyUrl,
    setValuePropositions,
    setIndustry,
    setService_ids,
    setBusinessCycle_ids,
    setFunctionalArea_ids,
    setSelectedFunctionalAreas,
    setStartDate,
    setEndDate,
  };

  return (
    <GenerateContext.Provider value={value}>
      {children}
    </GenerateContext.Provider>
  );
};

// Helper hook to use the context
export const useGenerateContext = () => {
  const context = useContext(GenerateContext);
  if (!context) {
    throw new Error(
      "useGenerateContext must be used within a GenerateProvider"
    );
  }
  return context;
};
