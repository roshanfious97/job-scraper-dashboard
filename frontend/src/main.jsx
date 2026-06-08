import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import logo from './assets/logo.png'

// set favicon from imported asset (Vite will resolve URL)
const setFavicon = (href, type = 'image/png') => {
  let link = document.querySelector("link[rel*='icon']") || document.createElement('link')
  link.type = type
  link.rel = 'icon'
  link.href = href
  const head = document.getElementsByTagName('head')[0]
  if (!document.querySelector("link[rel*='icon']")) head.appendChild(link)
}

setFavicon(logo, 'image/png')

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
