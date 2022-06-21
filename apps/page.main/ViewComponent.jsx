import MainView from "./VAComponent";
import React, { useState, } from "react";

const Main = () => {
    const [value, setValue] = useState("");
    console.log("this is react main component");

    const props = {
        value,
        setValue: e => {
            setValue(e.target.value);
        },
    }

    return <MainView {...props} />;
}

export default Main;
