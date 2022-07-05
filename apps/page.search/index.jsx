
/* WIZ-REACT APP API
 * additional options is refer to 
 * https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch
 */

const __initSearch__ = () => {
    const defaultOptions = {
        method: "GET",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    };

    const __onError__ = (err) => {
        console.error(err);
    }

    const URI = (apiName) => {
        return `/app/api/page.search/${apiName}`;
    }

    const API = async (apiName, options = {}, json = true, errorDefault = null, onError = __onError__) => {
        const opts = {
            ...defaultOptions,
            ...options,
        };
        try {
            let res = await fetch(URI(apiName), opts);
            if (!json) return res;
            const { code, data } = await res.json();
            if(!/^20[0124]$/.test(code)) {
                throw new Error(data);
            }
            return data;
        }
        catch(err) {
            onError(err);
            return errorDefault;
        }
    }

    return {
        API,
        lang: () => {
            return navigator.language;
        },
    };
}
const wiz = __initSearch__();

import { useRecoilState as wizState, useRecoilValue as wizValue } from "recoil";
import Directive from "WizDirective";
import "./view.scss";
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

const Search = () => {
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

    return (<Directive>
<div>
    this is Search page
    <input
        onChange={(e) => {
            setValue(e.target.value);
        }}
        value={value}
    />
    <div>value: {value}</div>
    <VAC name="recoil test" data={{rand, length}} />
    <div className="iftest" wiz-if={value.length > 0}>length over 0</div>
    <div className="iftest" wiz-if={value.length === 0}>length is 0</div>
    <hr/>
    <div className="fortest" wiz-for={['apple', 'banana', 'candy']}>
        <Test>
            <div wiz-for={['duty', 'earn', 'fist']}>
                <Test />
            </div>
        </Test>
    </div>
    <hr/>
    <div className="fortest" wiz-for={{a: 1, b: 2, c: 3}}>
        <Test2 />
    </div>
</div>
</Directive>);
}


export default Search