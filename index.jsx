import React from "react";
import ReactDOM from "react-dom/client";
import Router from "WizRouter";
import { RecoilRoot } from "recoil";
const App = () => {
    return (
        <RecoilRoot>
            <Router />
        </RecoilRoot>
    );
}
ReactDOM.createRoot(document.querySelector("#root")).render(<App />);