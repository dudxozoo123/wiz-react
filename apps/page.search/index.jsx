
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

import React from "react";
import { useRecoilState as wizState, useRecoilValue as wizValue } from "recoil";
import Directive from "WizDirective";
import "./view.scss";
const Search = () => {
   return (<Directive>

<div className="search-wrap">
  <table className="table table-hover">
    <thead>
      <th>
        <th>ID</th>
        <th>Name</th>
        <th>Created</th>
      </th>
    </thead>
    <tbody>
      <tr>
        <td>1</td>
        <td>철수</td>
        <td>20201</td>
      </tr>
    </tbody>
  </table>
</div>
</Directive>);
}

export default Search