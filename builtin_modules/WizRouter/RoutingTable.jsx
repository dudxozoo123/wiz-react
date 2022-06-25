import React from "react";
import Main from "page.main";
// import Search from "page.search";

const RouteTable = [
    {
        path: "/main",
        element: <Main />,
    },
    // {
    //     path: "/search/:type",
    //     element: Search,
    // },
];

export const RedirectTable = [
    {
        from: "*",
        to: "/main",
    },
];

export default RouteTable;
