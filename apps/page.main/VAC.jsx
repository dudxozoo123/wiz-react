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