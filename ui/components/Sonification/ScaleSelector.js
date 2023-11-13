"use client"

import * as React from "react"
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"
import { GlobalContext } from "@/context/GlobalContext"

const ScaleSelector = () => {
    const { globalState, setGlobalState } = React.useContext(GlobalContext)

    const handleOnValueChange = (scale) => {
        setGlobalState({ ...globalState, request: {...globalState?.request, scale: scale}})
    }

    return (
        <>
            <Label htmlFor="scale">Scale</Label>
            <Select onValueChange={handleOnValueChange} defaultValue={ globalState.response.scale }>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Select a scale" />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="default">Default</SelectItem>
                        <SelectItem value="chromatic">Chromatic</SelectItem>
                        <SelectItem value="blues">Blues</SelectItem>
                        <SelectItem value="a-sharp">A#</SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
        </>
    )
}

export default ScaleSelector
