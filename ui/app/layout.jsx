'use client'

import { Inter } from 'next/font/google'
import './globals.css'
import { GlobalContext, defaultGlobalState } from "@/context/GlobalContext"
import { useState } from 'react'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({ children }) {
  const [globalState, setGlobalState] = useState(defaultGlobalState)

  return (
    <html lang="pt-br">
      <body className={inter.className}>
        <div className="flex flex-col h-screen justify-between">
          <GlobalContext.Provider value={{globalState, setGlobalState }}>
            {children}
          </GlobalContext.Provider>
        </div>
      </body>
    </html>
  )
}
