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