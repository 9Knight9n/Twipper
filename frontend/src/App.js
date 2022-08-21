import { BrowserRouter,Routes, Route, Navigate } from "react-router-dom";
import { Result, Button } from 'antd';
import { SmileOutlined } from '@ant-design/icons';

// css
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

// views
import ExtractPage from "./pages/extractPage/ExtractPage";
import SelectCollection from "./pages/extractPage/SelectCollection";
import SelectUser from "./pages/extractPage/SelectUser";
import ExtractProgress from "./pages/extractPage/ExtractProgress";
import ResultPage from "./pages/resultPage/resultPage";
import CollectionAnalysis from "./pages/resultPage/collectionAnalysis/collectionAnalysis";
import UserAnalysis from "./pages/resultPage/userAnalysis/userAnalysis";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<Navigate to="extract" replace />}/>
        <Route path="extract" element={<ExtractPage />} >
            <Route index element={<Navigate to="selectcollection" replace />} />
            <Route path={'selectcollection'} element={<SelectCollection/>} />
            <Route path={'selectuser/:collection'} element={<SelectUser/>} />
            <Route path={'extractprogress/:collection'} element={<ExtractProgress/>} />
            <Route path="*" element={<Navigate to="selectcollection" replace />} />
        </Route>
        <Route path="result" element={<ResultPage />} >
            <Route path={"useranalysis/:collection"} element={<UserAnalysis/>} />
            <Route path={"collectionanalysis/:collection"} element={<CollectionAnalysis/>} />
        </Route>
        <Route path="*" element={<Navigate to="extract" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
