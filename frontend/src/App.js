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
        <Route path="done" element={<Result icon={<SmileOutlined />} title="مجموعه مدنظر اضافه شد." extra={<Button type="primary">تمام</Button>} />} />
        {/*<Route path="*" element={<Navigate to="extract" replace />} />*/}
      </Routes>
    </BrowserRouter>
  );
}

export default App;
