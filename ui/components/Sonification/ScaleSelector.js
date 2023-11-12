"use client"

import * as React from "react"
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Label } from "@/components/ui/label"

const ScaleSelector = () => {

    const handleOnValueChange = (event) => {
        console.log(event)
    }

    return (
        <>
            <Label htmlFor="temperature">Scale</Label>
            <Select onValueChange={handleOnValueChange} defaultValue="default">
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
