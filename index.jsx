import React from "react";
import ReactDOM from "react-dom/client";
import { RecoilRoot } from "recoil";
import Main from "./apps/page.main";
const App = () => {
    return (
        <RecoilRoot>
            <Main />
        </RecoilRoot>
    );
}
ReactDOM.createRoot(document.querySelector("#root")).render(<App />);