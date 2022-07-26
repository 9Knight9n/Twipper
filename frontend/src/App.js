import { BrowserRouter,Routes, Route } from "react-router-dom";

// css
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// views
import ExtractPage from "./pages/extractPage/ExtractPage";
import SelectCollection from "./pages/extractPage/SelectCollection";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="extract" element={<ExtractPage />} >
            <Route path={'selectcollection'} element={<SelectCollection/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
