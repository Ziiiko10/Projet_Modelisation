import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MainLayout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Scenarios } from './pages/Scenarios';
import { Analysis } from './pages/Analysis';
import { Settings } from './pages/Settings';

function App() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scenarios" element={<Scenarios />} />
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}

export default App;
