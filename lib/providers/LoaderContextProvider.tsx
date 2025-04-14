"use client";

import React, {
    ReactNode,
    createContext,
    useContext,
    useState
} from "react";

type LoaderState = {
  isLoading: boolean;
};

const LoaderContext = createContext<
  | {
      loaderState: LoaderState;
      startLoading: () => void;
      stopLoading: () => void;
    }
  | undefined
>(undefined);

export const useLoader = () => {
  const context = useContext(LoaderContext);
  if (!context) {
    throw new Error("useLoader must be used within a LoaderProvider");
  }
  return context;
};

export const LoaderProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [loaderState, setLoaderState] = useState<LoaderState>({
    isLoading: false,
  });

  const startLoading = () => {
    setLoaderState({ isLoading: true });
  };

  const stopLoading = (error?: Error) => {
    setLoaderState({ isLoading: false });
  };

  return (
    <LoaderContext.Provider value={{ loaderState, startLoading, stopLoading }}>
      {children}
    </LoaderContext.Provider>
  );
};
