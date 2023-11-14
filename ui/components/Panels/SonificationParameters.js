'use client'

import React from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "../ui/card"
import ScaleSelector from "@/components/Sonification/ScaleSelector"
import InstrumentSelector from "@/components/Sonification/InstrumentSelector"
import LayerComposeStrategySelector from "@/components/Sonification/LayerComposeStrategySelector"
import BPMSelector from "@/components/Sonification/BPMInput"
import { Button } from "@/components/ui/button"
import { PiArrowClockwiseBold, PiDnaBold, PiGuitarBold } from "react-icons/pi"
import { Separator } from "@radix-ui/react-separator"

const SonificationParameters = () => {
    return (
        <Card style={{border: 'none'}} className="shadow-none">
            <CardHeader>
                <CardTitle>Sonification parameters</CardTitle>
                <CardDescription>
                    It's possibile to specify sonification parameters to generate a different audio set.
                </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-6">
                <div className="flex-col space-y-4">
                    <ScaleSelector />

                    <Separator />

                    <BPMSelector />

                    <Separator />

                    <div className="flex items-center">
                        <span className="text-base font-medium">Layers</span>
                    </div>

                    <Card>
                        <CardContent className="p-4">
                            <p className="text-sm mb-4">1.</p>
                            <div className="flex items-center mb-4">
                                <PiGuitarBold className="mr-3" />
                                <InstrumentSelector instrument={23} />
                            </div>
                            <div className="flex items-center">
                                <PiDnaBold className="mr-3" />
                                <LayerComposeStrategySelector defaultValue={"0"} />
                            </div>
                        </CardContent>
                    </Card>
                    <Card className="bg-indigo-500g-gray-900">
                        <CardContent className="p-4">
                            <p className="text-sm mb-4">2.</p>
                            <div className="flex items-center mb-4">
                                <PiGuitarBold className="mr-3" />
                                <InstrumentSelector instrument={51} />
                            </div>
                            <div className="flex items-center">
                                <PiDnaBold className="mr-3" />
                                <LayerComposeStrategySelector defaultValue={"1"} />
                            </div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardContent className="p-4">
                            <p className="text-sm mb-4">3.</p>
                            <div className="flex items-center mb-4">
                                <PiGuitarBold className="mr-3" />
                                <InstrumentSelector instrument={14} />
                            </div>
                            <div className="flex items-center">
                                <PiDnaBold className="mr-3" />
                                <LayerComposeStrategySelector defaultValue={"2"} />
                            </div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardContent className="p-4">
                            <p className="text-sm mb-4">4.</p>
                            <div className="flex items-center mb-4">
                                <PiGuitarBold className="mr-3" />
                                <InstrumentSelector instrument={142} />
                            </div>
                            <div className="flex items-center">
                                <PiDnaBold className="mr-3" />
                                <LayerComposeStrategySelector defaultValue={"3"} />
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </CardContent>
            <CardFooter>
                <Button>
                    <PiArrowClockwiseBold className="mr-1" />
                    Update
                </Button>
            </CardFooter>
        </Card>
    )
}

export default SonificationParameters
