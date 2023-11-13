"use client"

import * as React from "react"
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { GlobalContext } from "@/context/GlobalContext"

const PresetSelector = () => {

    const { globalState, setGlobalState } = React.useContext(GlobalContext)

    const handleOnValueChange = (preset) => {
        setGlobalState({...globalState, preset: preset })
    }

    return (
        <>
            <Select onValueChange={handleOnValueChange}>
                <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="Load from a preset" />
                </SelectTrigger>
                <SelectContent>
                    <SelectGroup>
                        <SelectItem value="sars-cov-2">Sars-Cov-2</SelectItem>
                        <SelectItem value="cannis-lupus-familiaris">Cannis Lupus Familiaris</SelectItem>
                        <SelectItem value="arthobacter-phage-herb">Arthobacter Phage Herb</SelectItem>
                        <SelectItem value="cannabis-sativa-amalgavirus">Cannabis Sativa Amalgavirus</SelectItem>
                    </SelectGroup>
                </SelectContent>
            </Select>
        </>
    )
}

export default PresetSelector
