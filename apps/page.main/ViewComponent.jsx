import Directive from "./ReactDirective";
import React, { useState, } from "react";
import VAC from "react-vac";

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
    const [value, setValue] = useState("");
    const rand = () => {
        setValue(Math.random());
    }

    return (<Directive>
<div>
    this is test page.
    <input onChange={e => setValue(e.target.value)} value={value} />
    <div>
        value: {value}
    </div>
    <div wiz-if={value.length > 0}>
        123123123
    </div>
    <div wiz-if={value.length === 0}>
        654654654
    </div>
    <div wiz-for={3}>
        <Test />
    </div>
    <hr />
    <div wiz-for={['apple', 'banana', 'candy']}>
        <Test>
            <div wiz-for={['duty', 'earn', 'fist']}>
                <Test />
            </div>
        </Test>
    </div>
    <hr />
    <div wiz-for={{a: 1, b: 2, c: 3}}>
        <Test2 />
    </div>
</div>
</Directive>);
}

export default Main;
