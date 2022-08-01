import React, { useState, useEffect } from "react";
import VAC from "react-vac";
import { testAtom, valueSelector } from "WizStore";
import TestModule from "TestModule";
import Search from "page.search";

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

window.app.controller('test-app', async ($sce, $scope, $timeout) => {
    $scope.text = "123123123";
    $scope.alert = () => {
        alert("!!!");
    }
})
.directive('text', function ($compile) {
    return {
        restrict: "AE",
        scope: {
            content: "=",
        },
        template: `<div>{{content}}</div>`,
    }
})
.directive('wizText', function ($compile) {
    return {
        restrict: "A",
        scope: {},
        template: "<div>{{text}}</div>",
        link: ($scope, elmt, attrs, ctrl) => {
            $scope.$parent.$watch(attrs.wizText, (val) => {
                $scope.text = val;
            });
            // $scope.text = $scope.$parent.$eval(attrs.wizText);
        }
    }
})
.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind('keydown keypress', function (event) {
            if (event.which === 13) {
                scope.$apply(function () {
                    scope.$eval(attrs.ngEnter);
                });
                event.preventDefault();
            }
        });
    };
})

const WizComponent = () => {
    const [value, setValue] = wizState(testAtom);
    const length = wizValue(valueSelector);


    const rand = () => {
        setValue(Math.random());
    }
    // console.log(TestModule)

    useEffect(() => {
        const fn = async () => {
            const data = await wiz.API("status", {a: 1, b: 2});
            // console.log(data);
        }
        fn();
    }, []);

    return WizView;
    // return (
    //     <div ng-controller="test-app">
    //         <input ng-model="text" ng-enter="alert()"/>
    //         <text content="text" />
    //     </div>
    // );
}

