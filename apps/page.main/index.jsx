import React from "react";
import ReactDOM from "react-dom/client";
import { RecoilRoot } from "recoil";
import Main from "./ViewComponent.jsx";
const App = () => {
    return (
        <RecoilRoot>
            <Main />
        </RecoilRoot>
    );
}
ReactDOM.createRoot(document.querySelector("#root")).render(<App />);