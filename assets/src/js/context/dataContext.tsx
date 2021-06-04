import React,{useState,createContext,useContext} from 'react'


export const DataContext=createContext({
  data:[{dealer:"",name:"",price:0,lat:0,lon:0}],
  position:{userLat:0,userLon:0}
})
export const DataOpeContext=createContext({
  setData:(_)=>{},
  setPosition:(_)=>{}
})

const dataProvider = ({children}) => {
  const [data,setData]=useState([{dealer:"",name:"",price:0,lat:0,lon:0}])
  const [position,setPosition]=useState({userLat:0,userLon:0})
  return(
    <DataContext.Provider value={{data,position}}>
      <DataOpeContext.Provider value={{setData,setPosition}}>
        {children}
      </DataOpeContext.Provider>
    </DataContext.Provider>
  )
}

export const useSetData=()=>useContext(DataOpeContext).setData
export const useSetPosition=()=>useContext(DataOpeContext).setPosition

export default dataProvider
