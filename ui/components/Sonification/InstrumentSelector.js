"use client"

import * as React from "react"
import { Select, SelectLabel, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Input } from "../ui/input"

const InstrumentSelector = ({ instrument }) => {

    const handleOnValueChange = (event) => {
        console.log(event)
    }

    return (
        <Input type="text" defaultValue={instrument} />
        // <Select onValueChange={handleOnValueChange} defaultValue="default">
        //     <SelectTrigger className="w-full">
        //         <SelectValue placeholder="Select a scale" />
        //     </SelectTrigger>
        //     <SelectContent>
        //         <SelectGroup className="overflow-y-auto h-32">
        //             <SelectLabel>Piano</SelectLabel>
        //             <SelectItem value="0">Acoustic Grand Piano</SelectItem>
        //             <SelectItem value="1">Bright Acoustic Piano</SelectItem>
        //             <SelectItem value="2">Electric Grand Piano</SelectItem>
        //             <SelectItem value="3">Honky-tonk Piano</SelectItem>
        //             <SelectItem value="4">Rhodes Piano</SelectItem>
        //             <SelectItem value="5">Chorused Piano</SelectItem>
        //             <SelectItem value="6">Harpsichord</SelectItem>
        //             <SelectItem value="7">Clavinet</SelectItem>
        //             <SelectItem value="0">Acoustic Grand Piano</SelectItem>
        //             <SelectItem value="1">Bright Acoustic Piano</SelectItem>
        //             <SelectItem value="2">Electric Grand Piano</SelectItem>
        //             <SelectItem value="3">Honky-tonk Piano</SelectItem>
        //             <SelectItem value="4">Rhodes Piano</SelectItem>
        //             <SelectItem value="5">Chorused Piano</SelectItem>
        //             <SelectItem value="6">Harpsichord</SelectItem>
        //             <SelectItem value="7">Clavinet</SelectItem>
        //             <SelectItem value="0">Acoustic Grand Piano</SelectItem>
        //             <SelectItem value="1">Bright Acoustic Piano</SelectItem>
        //             <SelectItem value="2">Electric Grand Piano</SelectItem>
        //             <SelectItem value="3">Honky-tonk Piano</SelectItem>
        //             <SelectItem value="4">Rhodes Piano</SelectItem>
        //             <SelectItem value="5">Chorused Piano</SelectItem>
        //             <SelectItem value="6">Harpsichord</SelectItem>
        //             <SelectItem value="7">Clavinet</SelectItem>
        //             <SelectItem value="0">Acoustic Grand Piano</SelectItem>
        //             <SelectItem value="1">Bright Acoustic Piano</SelectItem>
        //             <SelectItem value="2">Electric Grand Piano</SelectItem>
        //             <SelectItem value="3">Honky-tonk Piano</SelectItem>
        //             <SelectItem value="4">Rhodes Piano</SelectItem>
        //             <SelectItem value="5">Chorused Piano</SelectItem>
        //             <SelectItem value="6">Harpsichord</SelectItem>
        //             <SelectItem value="7">Clavinet</SelectItem>
        //         </SelectGroup>
        //     </SelectContent>
        // </Select>
    )
}

export default InstrumentSelector
