import { atom, selector } from 'recoil';

export const testAtom = atom({
    key: 'test',
    default: "this is test atom value",
});

export const valueSelector = selector({
    key: 'value',
    get: ({ get }) => {
        const value = "" + get(testAtom);
        return value.length;
    },
});

export default {
    testAtom,
    valueSelector,
};
