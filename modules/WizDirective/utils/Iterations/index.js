import { cloneElement } from "react";
import DIRECTIVE from "../enum";

const iterations = (child, keepDataAttributes) => {
  if (Array.isArray(child)) {
    return child.map(c => iterations(c, keepDataAttributes));
  }
  if (child && child.props && child.props.hasOwnProperty(DIRECTIVE.FOR)) {
    const iteration = child.props[DIRECTIVE.FOR];
    return getChildren(child, iteration, keepDataAttributes);
  } else if (child && child.props && child.props.children) {
    return {
      ...child,
      props: {
        ...child.props,
        [DIRECTIVE.FOR]:
          child.props[DIRECTIVE.FOR] && keepDataAttributes
            ? child.props[DIRECTIVE.FOR]
            : undefined,
        children: iterations(child.props.children, keepDataAttributes)
      }
    };
  }
  return child;
};

const getChildren = (child, iteration, keepDataAttributes) => {
  const { children } = child.props;
  const isReactElement = children.$$typeof.toString() === "Symbol(react.element)";
  if (typeof children === 'function' || typeof children === 'object') {
    if (Array.isArray(iteration)) {
      return iteration.map((it, ind) => {
        // let executedChild = children(it, ind);
        let executedChild = cloneElement(children, { item: it, $index: ind });
        if (executedChild.props && executedChild.props.children) {
          executedChild = getExecutedChildren(
            executedChild,
            keepDataAttributes
          );
        }
        return getChild(child, executedChild, keepDataAttributes);
      });
    } else if (typeof iteration === 'number' && !isNaN(iteration)) {
      return Array(iteration)
        .fill()
        .map((val, ind) => {
          // let executedChild = children(ind + 1, ind);
          let executedChild = cloneElement(children, { item: ind + 1, $index: ind });
          if (executedChild.props && executedChild.props.children) {
            executedChild = getExecutedChildren(
              executedChild,
              keepDataAttributes
            );
          }
          return getChild(child, executedChild, keepDataAttributes);
        });
    } else if (typeof iteration === 'object') {
      return Object.keys(iteration).map((k, ind) => {
        // let executedChild = children(iteration[k], k, ind);
        // let executedChild = cloneElement(children, { item: [k, iteration[k]], index: ind });
        let executedChild = cloneElement(children, { item: { key: k, value: iteration[k] }, $index: ind });
        if (executedChild.props && executedChild.props.children) {
          executedChild = getExecutedChildren(
            executedChild,
            keepDataAttributes
          );
        }
        return getChild(child, executedChild, keepDataAttributes);
      });
    }
  } else {
    const childIterations = [];
    const childPassed = {
      ...child,
      props: {
        ...child.props,
        [DIRECTIVE.FOR]:
          child.props[DIRECTIVE.FOR] && keepDataAttributes
            ? child.props[DIRECTIVE.FOR]
            : undefined,
        children: iterations(
          childIterations.length ? childIterations : children,
          keepDataAttributes
        )
      }
    };
    const childrenPassed = [];
    if (Array.isArray(iteration)) {
      iteration.forEach(() => childrenPassed.push(childPassed));
    } else if (typeof iteration === 'number') {
      for (let x = 1; x <= iteration; x++) {
        childrenPassed.push(childPassed);
      }
    } else if (typeof iteration === 'object') {
      for (let x = 1; x <= Object.keys(iteration); x++) {
        childrenPassed.push(childPassed);
      }
    }
    return childrenPassed.length ? childrenPassed : child;
  }

  return child;
};

const getExecutedChildren = (executedChild, keepDataAttributes) => {
  return {
    ...executedChild,
    props: {
      ...executedChild.props,
      [DIRECTIVE.FOR]:
        executedChild.props[DIRECTIVE.FOR] && keepDataAttributes
          ? executedChild.props[DIRECTIVE.FOR]
          : undefined,
      children: iterations(executedChild.props.children, keepDataAttributes)
    }
  };
};

const getChild = (child, executedChild, keepDataAttributes) => {
  return {
    ...child,
    props: {
      ...child.props,
      [DIRECTIVE.FOR]:
        child.props[DIRECTIVE.FOR] && keepDataAttributes
          ? child.props[DIRECTIVE.FOR]
          : undefined,
      children: executedChild
    }
  };
};

export default iterations;
