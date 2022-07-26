import { BrowserRouter,Routes, Route, Navigate } from "react-router-dom";

// css
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// views
import ExtractPage from "./pages/extractPage/ExtractPage";
import SelectCollection from "./pages/extractPage/SelectCollection";
import SelectUser from "./pages/extractPage/SelectUser";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Navigate to="extract" replace />}/>
        <Route path="extract" element={<ExtractPage />} >
            <Route index element={<Navigate to="selectcollection" replace />} />
            <Route path={'selectcollection'} element={<SelectCollection/>} />
            <Route path={'selectuser'} element={<SelectUser/>} />
            <Route path="*" element={<Navigate to="selectcollection" replace />} />
        </Route>
        <Route path="*" element={<Navigate to="extract" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
