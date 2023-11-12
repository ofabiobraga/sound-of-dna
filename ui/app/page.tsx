'use client'

import { PiDnaBold, PiFileDashedDuotone } from "react-icons/pi";
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { PresetSelector } from "./components/preset-selector"
import { Input } from "@/components/ui/input"
import { presets } from "./data/presets"
import { useRef, useState } from "react"
import LoadingSpinner from "./components/loading-spinner"
import GeneratedAudioData from "@/components/Panels/GeneratedAudioData"
import SonificationParameters from "@/components/Panels/SonificationParameters"

export default function PlaygroundPage() {
  const fileInput = useRef(null)
  const [isLoading, setIsLoading] = useState(false)
  const [sonificationData, setSonificationData] = useState(undefined)

  /**
   * Sends the selected files to the server.
   * 
   * @param event
   */
  const handleFileUpload = async (event: any) => {
    if (!event.target.files || !event.target.files[0]) {
      return
    }

    setIsLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', event.target.files[0])

      const response = await fetch('http://127.0.0.1:8000', {
        method: "POST",
        body: formData
      })

      if (response.ok) {
        const responseBody = await response.json()
        setSonificationData(responseBody)
        console.log(responseBody)
      }
    } catch (error) {
      console.log(error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
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
          {!sonificationData && <div className="flex items-center justify-center rounded-md border mb-6 p-4">
            <div className="mx-auto flex flex-col items-center justify-center text-center">
              <PiFileDashedDuotone size="3em" />

              <h3 className="mt-4 text-lg font-semibold">Submit a .fasta file to start</h3>
              <p className="mb-4 mt-2 text-sm text-muted-foreground">
                System is going to process your file and deliver the audio data.
              </p>

              {isLoading && <LoadingSpinner />}

              {!isLoading && <div className="flex items-center">
                <Button size="sm" className="relative m-3" onClick={() => fileInput.current.click()}>
                  Upload
                </Button>
                <Input id="file" type="file" onChange={handleFileUpload} ref={fileInput} style={{ display: 'none' }} accept=".fasta" />
                <span className="mr-3">or</span>
                <PresetSelector presets={presets} />
              </div>}
            </div>
          </div>}

          {/* After File  got Uploaded  */}
          {sonificationData && <div className="grid items-center gap-6 mb-6">
            <div className="flex flex-col space-y-4">
              <div className="grid gap-6 grid-cols-2">
                <SonificationParameters />
                <GeneratedAudioData mp3={sonificationData.mp3} midi={sonificationData.midi} json={sonificationData.json}  />
              </div>
            </div>
          </div>}
        </div>
      </div>
    </>
  )
}