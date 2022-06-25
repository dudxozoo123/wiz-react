import "./view.scss";
import Directive from "WizDirective";
import { useRecoilState as wizState, useRecoilValue as wizValue } from "recoil";
import React, { useState, } from "react";
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


// Main로 강제시키고 title로 replace
const Main = () => {
    const [value, setValue] = wizState(testAtom);
    const length = wizValue(valueSelector);
    const rand = () => {
        setValue(Math.random());
    }
    console.log(TestModule)

    return (<Directive>

<div>this is test page.
  <input onChange={e => setValue(e.target.value)} value={value}/>
  <div>value: {value}</div>
  <VAC name="recoil test" data={{rand, length}}></VAC>
  <div wiz-if={value.length > 0} class="iftest">length over 0</div>
  <div wiz-if={value.length === 0} class="iftest">length is 0</div>
  <div wiz-for={3} class="fortest">
    <Test></Test>
  </div>
  <hr/>
  <div wiz-for={['apple', 'banana', 'candy']} class="fortest">
    <Test>
      <div wiz-for={['duty', 'earn', 'fist']}>
        <Test></Test>
      </div>
    </Test>
  </div>
  <hr/>
  <div wiz-for={{a: 1, b: 2, c: 3}} class="fortest">
    <Test2></Test2>
  </div>
</div>
</Directive>);
}

export default Main;
