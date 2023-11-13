"use client"

import * as React from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@radix-ui/react-label"
import { GlobalContext } from "@/context/GlobalContext"

const BPMInput = () => {
    const { globalState, setGlobalState } = React.useContext(GlobalContext)

    const handleOnValueChange = (event) => {
        setGlobalState({...globalState, bpm: parseInt(event.target.value)})
    }

    return (
        <>
            <Label>BPM</Label>
            <Input type="number" onChange={handleOnValueChange} defaultValue={globalState.response.bmp ?? 140} max={240} />
        </>

    )
}

export default BPMInput
