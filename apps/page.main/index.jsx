import React from "react";
import ReactDOM from "react-dom/client";
import Main from "./ViewComponent.jsx";
const App = () => {
    return (
        <div className="react">
            <Main />
        </div>
    );
}
ReactDOM.createRoot(document.querySelector("#root")).render(<App />);