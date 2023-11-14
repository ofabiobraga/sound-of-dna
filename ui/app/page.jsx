'use client'

import { PiDnaBold, PiFileDashedDuotone } from "react-icons/pi";
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Input } from "@/components/ui/input"
import { useContext, useRef, useState } from "react"
import LoadingSpinner from "./components/loading-spinner"
import GeneratedAudioData from "@/components/Panels/GeneratedAudioData"
import SonificationParameters from "@/components/Panels/SonificationParameters"
import PresetSelector from "@/components/PresetSelector"
import { GlobalContext } from "@/context/GlobalContext";


export default function PlaygroundPage() {
  const fileInput = useRef(null)
  const {globalState, setGlobalState } = useContext(GlobalContext)
  
  /**
   * Sends the selected files to the server.
   * 
   * @param event
   */
  const handleFileUpload = async (event) => {
    if (!event.target.files || !event.target.files[0]) {
      return
    }

    setGlobalState({
      ...globalState,
      isLoading: true
    })

    const formData = new FormData()
    formData.append('file', event.target.files[0])

    const response = await fetch('http://127.0.0.1:8000', {
      method: "POST",
      body: formData
    })

    response.json().then((json) => {
      setGlobalState({
        ...globalState,
        response: json,
        isLoading: false
      })
    })
  }

  console.log(globalState)

  return (
    <GlobalContext.Provider value={{ globalState, setGlobalState }}>
      <div className="h-full flex-col flex">
        <div className="container flex flex-col items-center justify-between space-y-2 py-4">
          <div className="flex items-center">
            <PiDnaBold size="1em" />
            <span className="text-lg ml-1">Sound of</span>
            <span className="text-lg font-semibold ml-1">DNA</span>
          </div>
        </div>
        <Separator />
        <div className="container h-full py-6">

          {/* First screen  */}
          {!globalState.response && <div className="flex items-center justify-center rounded-md border mb-6 p-4">
            <div className="mx-auto flex flex-col items-center justify-center text-center">
              <PiFileDashedDuotone size="3em" />

              <h3 className="mt-4 text-lg font-semibold">Submit a .fasta file to start</h3>
              <p className="mb-1 mt-2 text-sm text-muted-foreground">
                System is going to process your file and deliver the audio data.
              </p>

              {globalState.isLoading && <LoadingSpinner />}

              {!globalState.isLoading && <div className="flex items-center">
                <Button size="sm" className="relative m-3" onClick={() => fileInput.current.click()}>
                  Upload
                </Button>
                <Input id="file" type="file" onChange={handleFileUpload} ref={fileInput} style={{ display: 'none' }} accept=".fasta" />
              </div>}
            </div>
          </div>}

          {/* After File  got Uploaded  */}
          {globalState.response && <div className="grid items-center gap-6 mb-6">
            <div className="flex flex-col space-y-4">
              <div className="grid gap-6 grid-cols-2">
                <SonificationParameters />
                <GeneratedAudioData />
              </div>
            </div>
          </div>}
        </div>
      </div>
    </GlobalContext.Provider>
  )
}