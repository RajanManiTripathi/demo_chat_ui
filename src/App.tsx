import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Chat from './pages/Chat'
import Rooms from './pages/Rooms'
import Settings from './pages/Settings'
import Personas from './pages/Personas'
import Prompts from './pages/Prompts'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="chat" element={<Chat />} />
        <Route path="rooms" element={<Rooms />} />
        <Route path="settings" element={<Settings />} />
        <Route path="personas" element={<Personas />} />
        <Route path="prompts" element={<Prompts />} />
      </Route>
    </Routes>
  )
}

export default App