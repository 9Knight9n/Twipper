import { BrowserRouter,Routes, Route } from "react-router-dom";
import './App.css';
import ExtractPage from "./pages/ExtractPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ExtractPage />} />
        {/*<Route path="about" element={<About />} />*/}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
