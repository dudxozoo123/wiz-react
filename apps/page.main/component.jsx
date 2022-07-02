import React, { useState, useEffect } from "react";
import VAC from "react-vac";
import { testAtom, valueSelector } from "WizStore";
import TestModule from "TestModule";

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
    console.log(TestModule)

    useEffect(() => {
        const fn = async () => {
            const data = await wiz.API("status", {a: 1, b: 2});
            console.log(data);
        }
        fn();
    }, []);

    return WizView;
}

export default Main;
