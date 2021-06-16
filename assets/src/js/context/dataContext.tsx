import React, { useState, createContext, useContext } from "react";

export const DataContext = createContext({
  data: [{ dealer: "", name: "", price: "", lat: 0, lon: 0 }],
  place: { userLat: 0, userLon: 0 },
});
export const DataOpeContext = createContext({
  setData: (_) => {},
  setPlace: (_) => {},
});

const dataProvider = ({ children }) => {
  const [data, setData] = useState([
    { dealer: "", name: "", price: "", lat: 0, lon: 0 },
  ]);
  const [place, setPlace] = useState({ userLat: 0, userLon: 0 });
  return (
    <DataContext.Provider value={{ data, place }}>
      <DataOpeContext.Provider value={{ setData, setPlace }}>
        {children}
      </DataOpeContext.Provider>
    </DataContext.Provider>
  );
};

export const useSetData = () => useContext(DataOpeContext).setData;
export const useSetPlace = () => useContext(DataOpeContext).setPlace;

export default dataProvider;
