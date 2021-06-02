import React,{useState,createContext,useContext} from 'react'

export const DataContext=createContext("")
export const DataOpeContext=createContext({setdata:(_)=>{}})

const dataProvider = ({children}) => {
  const [data,setData] =useState("")
  const setdata=(d)=>setData(d);
  return(
    <DataContext.Provider value={data}>
      <DataOpeContext.Provider value={{setdata}}>
        {children}
      </DataOpeContext.Provider>
    </DataContext.Provider>
  )
}

export const useSetData=()=>useContext(DataOpeContext).setdata

export default dataProvider
