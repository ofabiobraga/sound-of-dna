"use client"

import * as React from "react"
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const LayerComposeStrategySelector = ({ defaultValue }) => {

    const handleOnValueChange = (event) => {
        console.log(event)
    }

    return (
        <Select onValueChange={handleOnValueChange} defaultValue={defaultValue}>
            <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a compose strategy" />
            </SelectTrigger>
            <SelectContent>
                <SelectGroup>
                    <SelectItem value="0">All codons</SelectItem>
                    <SelectItem value="1">All codons with start/stop</SelectItem>
                    <SelectItem value="2">Polar codons only</SelectItem>
                    <SelectItem value="3">All di-nucleotides</SelectItem>
                    <SelectItem value="4">Basic codons with start/stop</SelectItem>
                </SelectGroup>
            </SelectContent>
        </Select>
    )
}

export default LayerComposeStrategySelector
