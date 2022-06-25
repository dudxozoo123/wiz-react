import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import RoutingTable, { RedirectTable } from "./RoutingTable";

const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                {RoutingTable.map((props, idx) => (
                    <Route
                        key={`route-${idx}`}
                        exact
                        {...props}
                    />
                ))}
                {RedirectTable.map(({ from, to }, idx) => (
                    <Route
                        key={`redirect-${idx}`}
                        path={from}
                        element={<Navigate replace to={to} />}
                    />
                ))}
            </Routes>
        </BrowserRouter>
    );
}

export default Router;
