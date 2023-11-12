"use client"

import * as React from "react"
import { Input } from "@/components/ui/input"
import { Label } from "@radix-ui/react-label"

const BPMInput = ({ layer }) => {

    const handleOnValueChange = (event) => {
        console.log(event)
    }

    return (
        <>
            <Label>BPM</Label>
            <Input type="number" defaultValue={150} max={240} />
        </>

    )
}

export default BPMInput
