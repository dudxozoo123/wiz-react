div
    | this is test page.
    input(onChange="{e => setValue(e.target.value)}" value="{value}")
    div value: {value}
    VAC(name="recoil test" data="{{rand, length}}")
    .iftest(wiz-if="{value.length > 0}") length over 0
    .iftest(wiz-if="{value.length === 0}") length is 0
    hr
    .fortest(wiz-for="{['apple', 'banana', 'candy']}")
        Test
            div(wiz-for="{['duty', 'earn', 'fist']}")
                Test
    hr
    .fortest(wiz-for="{{a: 1, b: 2, c: 3}}")
        Test2
