import { BrowserRouter,Routes, Route } from "react-router-dom";

// css
import './App.css';

// views
import ExtractPage from "./pages/extractPage/ExtractPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ExtractPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
