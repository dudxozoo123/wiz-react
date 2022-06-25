import React, { useState, } from "react";
import VAC from "react-vac";
import { testAtom, valueSelector } from "./Store";

const Test = ({ children, item, $index }) => {
    return (
        <div>
            this is test.
            <div>{item}-{$index}</div>
            {children}
            <hr />
        </div>
    );
}
const Test2 = ({ item, $index }) => {
    // const [key, value] = item;
    const { key, value } = item;
    return (
        <div>
            this is test.
            <div>{key}-{value}-{$index}</div>
        </div>
    );
}


// WizComponent로 강제시키고 title로 replace
const Main = () => {
    const [value, setValue] = wizState(testAtom);
    const length = wizValue(valueSelector);
    const rand = () => {
        setValue(Math.random());
    }

    return WizView;
}

export default Main;
