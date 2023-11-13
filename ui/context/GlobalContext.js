'use client'

import { createContext } from 'react'

export const defaultGlobalState = {
    isLoading: false,
    preset: null,
    response: null,
    request: {
        'scale': 'default',
        'bmp': 140,
        'instruments': [],
        'strategies': []
    }
}

export const GlobalContext = createContext(defaultGlobalState)